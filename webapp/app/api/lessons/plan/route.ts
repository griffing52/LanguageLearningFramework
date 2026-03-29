import { useCases } from "@/src/server/composition";
import { PlanLessonRequest } from "@/src/shared/contracts/api";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as PlanLessonRequest;

    if (!body.learnerId || !body.languageCode || !body.targetGoal) {
      return Response.json(
        { error: "learnerId, languageCode, and targetGoal are required." },
        { status: 400 },
      );
    }

    const plan = await useCases.planNextLesson.execute(body);

    return Response.json(plan, { status: 200 });
  } catch {
    return Response.json(
      { error: "Unable to create a lesson plan." },
      { status: 500 },
    );
  }
}
