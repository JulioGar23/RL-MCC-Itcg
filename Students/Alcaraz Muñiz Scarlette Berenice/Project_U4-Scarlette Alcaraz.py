#!/usr/bin/env python3

import numpy as np
import gymnasium as gym
from dataclasses import dataclass
import typing as tt

import torch
import torch.nn as nn
import torch.optim as optim

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import deque

# ─────────────────────────────────────────
# HYPERPARAMETERS
# ─────────────────────────────────────────
HIDDEN_SIZE = 128
BATCH_SIZE  = 16
PERCENTILE  = 70
MAX_HISTORY = 100

# ─────────────────────────────────────────
# NEURAL NETWORK
# ─────────────────────────────────────────
class Net(nn.Module):
    def __init__(self, obs_size: int, hidden_size: int, n_actions: int):
        super(Net, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


# ─────────────────────────────────────────
# DATACLASSES
# ─────────────────────────────────────────
@dataclass
class EpisodeStep:
    observation: np.ndarray
    action: int

@dataclass
class Episode:
    reward: float
    steps: tt.List[EpisodeStep]


# ─────────────────────────────────────────
# BATCH GENERATOR
# ─────────────────────────────────────────
def iterate_batches(
    env: gym.Env,
    net: Net,
    batch_size: int
) -> tt.Generator[tt.List[Episode], None, None]:
    batch          = []
    episode_reward = 0.0
    episode_steps  = []
    obs, _         = env.reset()
    sm             = nn.Softmax(dim=1)

    while True:
        obs_v       = torch.tensor(obs, dtype=torch.float32)
        act_probs_v = sm(net(obs_v.unsqueeze(0)))
        act_probs   = act_probs_v.data.numpy()[0]
        action      = np.random.choice(len(act_probs), p=act_probs)

        next_obs, reward, is_done, is_trunc, _ = env.step(action)
        episode_reward += float(reward)
        episode_steps.append(EpisodeStep(observation=obs, action=action))

        if is_done or is_trunc:
            batch.append(Episode(reward=episode_reward, steps=episode_steps))
            episode_reward = 0.0
            episode_steps  = []
            next_obs, _    = env.reset()

            if len(batch) == batch_size:
                yield batch
                batch = []

        obs = next_obs


# ─────────────────────────────────────────
# PERCENTILE FILTER
# ─────────────────────────────────────────
def filter_batch(
    batch: tt.List[Episode],
    percentile: float
) -> tt.Tuple[torch.FloatTensor, torch.LongTensor, float, float]:
    rewards      = [e.reward for e in batch]
    reward_bound = float(np.percentile(rewards, percentile))
    reward_mean  = float(np.mean(rewards))

    train_obs: tt.List[np.ndarray] = []
    train_act: tt.List[int]        = []

    for episode in batch:
        if episode.reward < reward_bound:
            continue
        train_obs.extend(step.observation for step in episode.steps)
        train_act.extend(step.action      for step in episode.steps)

    train_obs_v = torch.FloatTensor(np.vstack(train_obs))
    train_act_v = torch.LongTensor(train_act)
    return train_obs_v, train_act_v, reward_bound, reward_mean


# ─────────────────────────────────────────
# PLOT SETUP
# ─────────────────────────────────────────
def setup_plot():
    """Creates the matplotlib window with 3 subplots."""
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(12, 7))
    fig.suptitle("Cross-Entropy Method — CartPole-v1", fontsize=14, color="white")

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    ax_reward = fig.add_subplot(gs[0, :])   # Row 0, both columns
    ax_loss   = fig.add_subplot(gs[1, 0])   # Row 1, left column
    ax_bound  = fig.add_subplot(gs[1, 1])   # Row 1, right column

    # Mean reward
    ax_reward.set_title("Mean Reward per Iteration", color="white")
    ax_reward.set_xlabel("Iteration")
    ax_reward.set_ylabel("Mean Reward")
    ax_reward.axhline(y=475, color="yellow", linestyle="--", linewidth=1, label="Goal (475)")
    ax_reward.legend(loc="upper left")

    # Loss
    ax_loss.set_title("Loss (Cross-Entropy Loss)", color="white")
    ax_loss.set_xlabel("Iteration")
    ax_loss.set_ylabel("Loss")

    # Reward bound
    ax_bound.set_title("Percentile 70 Threshold", color="white")
    ax_bound.set_xlabel("Iteration")
    ax_bound.set_ylabel("Reward Bound")

    plt.ion()       # Interactive mode: allows updates without blocking
    plt.show()
    return fig, ax_reward, ax_loss, ax_bound


def update_plot(fig, ax_reward, ax_loss, ax_bound,
                iters, means, losses, bounds):
    """Redraws the plots with the latest data."""
    ax_reward.clear()
    ax_reward.set_title("Mean Reward per Iteration", color="white")
    ax_reward.set_xlabel("Iteration")
    ax_reward.set_ylabel("Mean Reward")
    ax_reward.axhline(y=475, color="yellow", linestyle="--", linewidth=1, label="Goal (475)")
    ax_reward.plot(iters, means, color="#00d4ff", linewidth=2, label="Mean Reward")
    ax_reward.fill_between(iters, means, alpha=0.15, color="#00d4ff")
    ax_reward.legend(loc="upper left")

    ax_loss.clear()
    ax_loss.set_title("Loss (Cross-Entropy Loss)", color="white")
    ax_loss.set_xlabel("Iteration")
    ax_loss.set_ylabel("Loss")
    ax_loss.plot(iters, losses, color="#ff6b6b", linewidth=2)
    ax_loss.fill_between(iters, losses, alpha=0.15, color="#ff6b6b")

    ax_bound.clear()
    ax_bound.set_title("Percentile 70 Threshold", color="white")
    ax_bound.set_xlabel("Iteration")
    ax_bound.set_ylabel("Reward Bound")
    ax_bound.plot(iters, bounds, color="#a8ff78", linewidth=2)
    ax_bound.fill_between(iters, bounds, alpha=0.15, color="#a8ff78")

    fig.canvas.draw()
    fig.canvas.flush_events()


# ─────────────────────────────────────────
# AGENT VIEWER
# ─────────────────────────────────────────
def watch_agent(net: Net, episodes: int = 3):
    """
    Opens a Gymnasium window with render_mode='human'
    and runs the trained agent for a given number of episodes.
    """
    print("\n🎮 Opening trained agent animation...")
    print(f"   Playing {episodes} episodes. Close the window to exit.\n")

    env_render = gym.make("CartPole-v1", render_mode="human")
    sm = nn.Softmax(dim=1)
    net.eval()

    for ep in range(episodes):
        obs, _ = env_render.reset()
        total_reward = 0.0
        steps = 0

        while True:
            obs_v     = torch.tensor(obs, dtype=torch.float32)
            act_probs = sm(net(obs_v.unsqueeze(0))).data.numpy()[0]
            action    = int(np.argmax(act_probs))   # Greedy action (best move)

            obs, reward, terminated, truncated, _ = env_render.step(action)
            total_reward += float(reward)
            steps += 1

            if terminated or truncated:
                print(f"   Episode {ep + 1}: {steps} steps | Reward: {total_reward:.0f}")
                break

    env_render.close()
    print("\n✅ Animation finished.")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    env = gym.make("CartPole-v1")
    assert env.observation_space.shape is not None
    obs_size  = env.observation_space.shape[0]
    assert isinstance(env.action_space, gym.spaces.Discrete)
    n_actions = int(env.action_space.n)

    net       = Net(obs_size, HIDDEN_SIZE, n_actions)
    objective = nn.CrossEntropyLoss()
    optimizer = optim.Adam(params=net.parameters(), lr=0.01)

    print(net)
    print("\n🚀 Starting training...\n")

    # History for plots
    hist_iters  = deque(maxlen=MAX_HISTORY)
    hist_means  = deque(maxlen=MAX_HISTORY)
    hist_losses = deque(maxlen=MAX_HISTORY)
    hist_bounds = deque(maxlen=MAX_HISTORY)

    fig, ax_reward, ax_loss, ax_bound = setup_plot()

    for iter_no, batch in enumerate(iterate_batches(env, net, BATCH_SIZE)):
        obs_v, acts_v, reward_b, reward_m = filter_batch(batch, PERCENTILE)

        optimizer.zero_grad()
        action_scores_v = net(obs_v)
        loss_v = objective(action_scores_v, acts_v)
        loss_v.backward()
        optimizer.step()

        loss_val = loss_v.item()

        print(f"{iter_no:3d}: loss={loss_val:.3f}  "
              f"reward_mean={reward_m:.1f}  "
              f"reward_bound={reward_b:.1f}")

        # Update history
        hist_iters.append(iter_no)
        hist_means.append(reward_m)
        hist_losses.append(loss_val)
        hist_bounds.append(reward_b)

        # Redraw plot every iteration
        update_plot(
            fig, ax_reward, ax_loss, ax_bound,
            list(hist_iters),
            list(hist_means),
            list(hist_losses),
            list(hist_bounds),
        )

        if reward_m > 475:
            print("\n✅ Solved!")
            break

    env.close()
    plt.ioff()
    plt.show(block=False)

    # ─────────────────────────────────────────
    # ANIMATION: watch the trained agent play
    # ─────────────────────────────────────────
    watch_agent(net)