from env.models import Observation, Action
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(a, b):
    emb1 = model.encode(a, convert_to_tensor=True)
    emb2 = model.encode(b, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2))

class SmartOpsEnv:

    def __init__(self, task):
        self.task = task
        self.current_index = 0
        self.done = False

    async def reset(self):
        self.current_index = 0
        self.done = False
        return self._get_observation()

    def _get_observation(self):
        ticket = self.task["tickets"][self.current_index]
        return Observation(
            ticket_id=ticket["id"],
            customer_message=ticket["message"],
            history=""
        )

    async def step(self, action: Action):
        ticket = self.task["tickets"][self.current_index]
        reward = self._compute_reward(ticket, action)

        self.current_index += 1
        if self.current_index >= len(self.task["tickets"]):
            self.done = True

        return {
            "observation": self._get_observation() if not self.done else None,
            "reward": reward,
            "done": self.done,
            "info": {}
        }

    def _compute_reward(self, ticket, action):
        reward = 0.0

        if action.priority == ticket["expected_priority"]:
            reward += 0.3

        if action.department == ticket["expected_department"]:
            reward += 0.3

        similarity = semantic_similarity(action.response, ticket["ideal_response"])
        reward += 0.3 * similarity

        if "don't know" in action.response.lower():
            reward -= 0.2

        return max(0.0, min(1.0, reward))

    def state(self):
        return {"index": self.current_index, "done": self.done}
