import sys
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file,encoding="utf-8") as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file,encoding="utf-8") as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # タイトルをpage_idに変換
    def convert_to_page_id(self,title):
        page_id = None
        for key in self.titles.keys():
            if self.titles[key] == title:
                page_id = key
        return page_id

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    # BFS（幅優先検索）を採用。　/　queue
    def find_shortest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #

        # 入力されたタイトルを、page_idに変換
        # タイトルに該当するページが存在しない場合は処理を中止
        start_id = self.convert_to_page_id(start)
        assert start_id != None
        goal_id = self.convert_to_page_id(goal) #
        assert goal_id != None

        # queueを定義
        queue = deque()

        # 探索済み（＝すでにqueueに追加済み）のページを「{現在のID: 1つ前のID}」の形式で記録する
        # これにより、重複した探索を防ぎつつ、ゴールからルートを逆にたどれる
        # スタートに当たるページの「1つ前のID」は "head" とする
        visited = {}
        visited[start_id] = "head"
        queue.append(start_id)

        answer_list = []

        # queueが空になるまでループ
        while not len(queue) == 0:
            curr = queue.popleft() # 現在先頭にあるノードをqueueから取り出し、currとして定義
            if curr == goal_id:
                while curr != "head":  # ゴールからルートを逆にたどり、ゴールに至るまでの経路を改めて記録
                    answer_list.insert(0,curr)
                    curr = visited[curr] # 1つ前のノードへ移動
                break
            for child in self.links[curr]: # currの子ノードをそれぞれqueueに追加し、visitedにも記録
                if child not in visited:
                    queue.append(child)
                    visited[child] = curr

        answer = {id:self.titles[id] for id in answer_list}
        print(answer)
        return answer

        #------------------------#


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #

        page_id_list = list(self.titles.keys()) # page__idのリストを取得
        rank_dict = {page_id: 1.0 for page_id in page_id_list} # wikipediaに存在するすべてのワードについて、初期値1を与える

        #　収束条件を満たすまで無限にループ
        while True:
            new_rank = {page_id: 0.15 for page_id in page_id_list} # 毎周、全員に配るベース値 (0.15) で初期化した辞書を作る

            # 各ノードのページランク*0.85を隣接ノードに均等に振り分ける
            for page_id in page_id_list:
                linked_page_ids = self.links[page_id] # 各ページについて、リンク先のpage_idのリストを取得
                counter = len(linked_page_ids) # 各ページについて、リンク先の個数を取得
                isolated_page_score_sum = 0

                # 各ページについて、リンク先が存在する場合
                if counter > 0:
                    give_score = (rank_dict[page_id] * 0.85) / counter

                    index = 0
                    while counter > index:
                        target_id = linked_page_ids[index]
                        if target_id in new_rank:
                            new_rank[target_id] += give_score
                        index += 1

                # 各ページについて、リンク先が存在しない場合(孤立ページ)
                else:
                    isolated_page_score_sum += (rank_dict[page_id] * 0.85) / len(page_id_list)

            # 貯めておいた孤立ページのスコアを、最後に一括で全ノードに足す
            if isolated_page_score_sum > 0:
                for page_id in page_id_list:
                    new_rank[page_id] += isolated_page_score_sum

            # 収束条件のチェック : ∑(new - old)^2
            diff_sum = 0.0
            for page_id in page_id_list:
                diff_sum += (new_rank[page_id] - rank_dict[page_id]) ** 2

            print(diff_sum)
            print(new_rank)

            # new_rankでrank_dictを更新
            rank_dict = new_rank

            # 変化量が0.01未満ならループを抜ける
            if diff_sum < 0.01:
                break

        # ループの外で結果を集計
        curr_score = [None, 0] # 初期値を [None, 0] に
        for key, value in rank_dict.items():
            if value >= curr_score[1]:
                curr_score[0] = key
                curr_score[1] = value

        curr_score.insert(1, self.titles[curr_score[0]])
        print(curr_score)

        return curr_score
        #------------------------#


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    # DFSでできる限り探索（最長のものを記録する）※BFSだと最長のものにたどり着くのが最後になってしまう？
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #

        # 入力されたタイトルを、page_idに変換
        start_id = self.convert_to_page_id(start)
        assert start_id is not None
        goal_id = self.convert_to_page_id(goal)
        assert goal_id is not None

        # スタックを定義
        # (現在のノードID, スタートからここまでに通ってきたルートのリスト):タプル
        stack = deque()
        stack.append((start_id, [start_id]))

        longest_answer_list = []

        # スタックが空になるまでループ
        while len(stack) > 0:
            # スタック末尾から現在のノードと、スタートからそのノードまでに通ってきたルートのリストを取り出す
            curr, current_path = stack.pop()

            # ゴールに到達した場合
            if curr == goal_id:
                # 現時点で最長の経路であれば一時保存
                if len(longest_answer_list) <= len(current_path):
                    longest_answer_list = current_path
                    print(longest_answer_list)
                continue # 以下の処理（子ノードを選択し、スタックに追加・・・）はスキップ　/　枝切り

            children = self.links[curr]

            # スタートからそのノードまでに通ってきたルートのリストにおいて、存在しないものだけを子ノードとして選ぶ
            set_current_path = set(current_path)
            children_not_visited = [item for item in children if item not in set_current_path]

            for child in children_not_visited:
                stack.append((child, current_path + [child]))

        # IDのリストをタイトルに変換
        answer = {id: self.titles[id] for id in longest_answer_list}
        print(answer)
        return answer
        #------------------------#


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])
        visited = {}
        for node in path:
            assert(node not in visited)
            visited[node] = True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    # wikipedia.find_shortest_path("渋谷", "小野妹子")
    # Homework #2
    # wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("C", "D")
