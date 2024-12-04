def timeslotBacktracking(pTimeslots):
    n = len(pTimeslots)
    result = []
    solution = []

    backtrackTimeslots(0, n, result, solution, pTimeslots)
    return result


def backtrackTimeslots(i, n, result, solution, timeslots):
    if i == n:
        result.append(solution[:])
        return
    
    backtrackTimeslots(i+1, n, result, solution, timeslots)

    solution.append(timeslots[i])
    backtrackTimeslots(i+1, n, result, solution, timeslots)
    solution.pop()




def teacherBacktracking(pAv, pTimeslots):
    n = len(pAv)
    ans = []
    sol = []

    backtrack(sol, n, ans, pAv, pTimeslots)

    return ans

def backtrack(sol, n, ans, av, pTimeslots):

    if len(ans) >= 8:  # Check if we have enough results
        return
    
    
    if len(sol) == n:
        ans.append(sol[:])
        return
    
    for teacher in av:
        if teacher[0] not in sol:

            sol.append(teacher[0])
            index = sol.index(teacher[0]) + 1
            if teacher[index] == 0:
                backtrack(sol, n, ans, av, pTimeslots)
            sol.pop()

    