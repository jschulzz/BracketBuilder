def findpaths(g, src, dst, writeGames=True, depth=5, others=[]):
    score = 0
    queue = []

    path = []
    path.append(src)
    queue.append((path, 0))
    suck_degree = 0
    while queue:
        data_point = queue.pop(0)
        # print(data_point)
        path = data_point[0]
        trans_score = data_point[1]
        last = path[len(path) - 1]
        if suck_degree > depth:
            return score
        if len(path) > suck_degree:
            suck_degree += 1
            if writeGames:
                print("Entering Degree", suck_degree, "of suck. Score at", score)
        others_contained = True
        for i in others:
            if i not in path:
                others_contained = False
        if last == dst and others_contained:
            if writeGames:
                printpath(data_point)
            score += scoreFn(suck_degree, data_point[1], len(path) - 1)

        # print(g, last)
        for team in g[last]:
            # print(team, path)
            # if team[0] not in path or team[0] == src:  # circle suck
            if team[0] not in path:  # non circle such
                newpath = list(path)
                newpath.append(team[0])
                queue.append((newpath, trans_score + team[1]))
