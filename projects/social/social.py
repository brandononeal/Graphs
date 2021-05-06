import random

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for i in range(0, num_users):
            self.add_user(f"User {i}")

        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}

        def dfs(friend, path):   
            if friend not in path:
                path.append(friend)

                for f in sg.friendships[friend]:
                    dfs(f, path)
            
            return path

        def dft(friend):
            if friend in visited:             
                return

            visited[friend] = dfs(user_id, [])

            for i, x in enumerate(visited[friend]):
                if x == friend:
                    del visited[friend][i+1::]

            for f in sg.friendships[friend]:
                dft(f)

        dft(user_id)

        return visited

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(f'\n{sg.friendships}')
    connections = sg.get_all_social_paths(1)
    print(f'\n{connections}')
