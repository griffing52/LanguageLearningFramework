import {
  LessonPlan,
  LessonPlannerPort,
  PlanNextLessonInput,
} from "@/src/modules/lesson-planner/domain/types";

export class PlanNextLessonUseCase {
  constructor(private readonly lessonPlanner: LessonPlannerPort) {}

  async execute(input: PlanNextLessonInput): Promise<LessonPlan> {
    return this.lessonPlanner.planNextLesson(input);
  }
}
