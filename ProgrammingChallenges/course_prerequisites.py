def canFinish(prerequisites):
  current_course = prerequisites[0]
  prerequisite_courses = []

  while current_course is not None:
    if current_course[0] in prerequisite_courses:
      return False

    current_course_prerequisites = [x for x in prerequisites[1:] if x[1] == current_course[0]]

    if current_course_prerequisites:
      current_course = current_course_prerequisites[0]
      prerequisite_courses.append(current_course[1])
    else:
      current_course = None

  return True

# [prerequisite, course]

prerequisites = [[1, 0], [2, 1], [3, 2], [1, 3]]
print(canFinish(prerequisites)) # False

prerequisites = [[1, 0], [2, 1], [3, 2]]
print(canFinish(prerequisites)) # True

prerequisites = [[1, 0], [2, 1], [3, 4], [1, 3]]
print(canFinish(prerequisites)) # True
