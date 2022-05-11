import numpy as np

import tensorflow as tf
from tensorflow.keras.layers import Dense, Activation, Input
from tensorflow.keras.optimizers import Adam


class Experience:

    def __init__(self, current_state, current_action, resulting_reward, resulting_state):
        """
        Holds the memory for replay
        :param current_state: the current state of the model
        :param current_action: the action that was chosen
        :param res_reward: the resulting reward
        :param res_state: the resulting state
        """
        self.current_state = current_state
        self.current_action = current_action
        self.res_reward = resulting_reward
        self.next_state = resulting_state


class ReplayMemory:
    """
    - Serves as a queue that has a max_size
    - Max size is by default None and should be added by the user
    """

    def __init__(self, max_size=None):
        self._max_size = max_size
        self._arr = []
        self._size = 0

    def add_experience(self, ex: Experience):
        if self._size == self._max_size and self._max_size is not None:
            self._arr.pop(0)
            self._size -= 1
        self._arr.append(ex)
        self._size += 1

    def get_random_experiences(self, num_samples):
        np.random.shuffle(self._arr)
        return self._arr[0:num_samples if num_samples < self._size else self._size]


class DeepQLearning:
    """
    - Deep Network Reference came from "Deep learning with tensorflow2 and Keras" - Antonio Gulli
    """

    def __init__(self, states: int, actions: int, alpha: float, epsilon: float, y: float, batch_size: int, replay_mem_max=10_000, threshold=-5):
        """

		:param states: number of states
		:param actions: number of actions that can be taken
		:param alpha: learning rate for updating states in Q-table
		:param y: scale factor for the bellman equation
		"""
        self.alpha = alpha
        self.y = y
        self._epsilon = epsilon
        self._t = 0  # time for exploration function
        self._actions = actions
        self._states = states
        self._threshold = threshold
        self._current_action = None
        self._current_state = None
        self._exploration_proba_decay = 0.005
        self.replay_memory = ReplayMemory(max_size=replay_mem_max)
        self._batch_size = batch_size
        model = tf.keras.models.Sequential()
        model.add(Dense(32, input_shape=(states,)))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(actions))
        self.model = model
        self.model.compile(loss="mse", optimizer=Adam(learning_rate=self.alpha))

    def update(self, state, reward) -> int:
        """
        :param current_state:
        :param reward:
        :return:
        """
        # update the t-value (time) [currently not being used]
        # for if exploration is a function of time
        self._t += 1
        # check to see if this is the first iteration (self._current_state and self._current_action are set to None)
        experience = Experience(self._current_state, self._current_action, reward, state)
        if self._current_state is not None:
            self.replay_memory.add_experience(experience)

        # update values for next iteration
        self._current_state = state

    def get_action(self, current_state):
        current_state = np.array(current_state).reshape(1, -1)
        if self.exploration_func(self._t):
            action = np.random.choice(range(self._actions))
            self._current_action = action
            return action
        pred = self.model.predict(current_state)[0]
        action = np.argmax(pred)
        self._current_action = action
        return action

    def train_model(self, batch_size = None):
        if batch_size is None:
            batch_size = self._batch_size

        """
        - Get [batch_size] number of experiences and train on those experiences
        """
        batch = self.replay_memory.get_random_experiences(batch_size)
        for ex in batch:

            current_state = np.array(ex.current_state).reshape(1, -1)
            # predict the q_vals
            q_val_prediction = self.model.predict(current_state)
            # set the target to be what the experience reward ACTUALLY was
            q_target = ex.res_reward
            next_state = np.array(ex.next_state).reshape(1, -1)
            # use the bellman equation to adjust the q_target
            q_target = q_target + self.y * np.max(self.model.predict(next_state)[0])
            # adjust the q_val at that action that was chosen, to be the actual value
            q_val_prediction[0][ex.current_action] = q_target
            # adjust the weights (no other q_vals are impacted)
            self.model.fit(current_state, q_val_prediction, verbose=2)


    def exploration_func(self, t) -> bool:
        """
        - Exploration can be changed to account for time
        :param t:
        :return: True for random search, False for highest value
        """
        p = np.random.uniform(0, 1)
        if p > self._epsilon:
            return True
        return False

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - Saving and loading learning model - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def save_model(self, path):
        """
        - Let the agent decide where to place the file
        """
        self.model.save_weights(path)

    def load_model(self, path):
        """
        - File path is specified in the agent
        """
        self.model.load_weights(path)
