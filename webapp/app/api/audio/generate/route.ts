import { useCases } from "@/src/server/composition";
import { GenerateAudioRequest } from "@/src/shared/contracts/api";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as GenerateAudioRequest;

    if (!body.lessonPlan) {
      return Response.json(
        { error: "lessonPlan is required." },
        { status: 400 },
      );
    }

    const lessonAudio = await useCases.generateAudioLesson.execute({
      lessonPlan: body.lessonPlan,
    });

    return Response.json(lessonAudio, { status: 200 });
  } catch {
    return Response.json(
      { error: "Unable to generate lesson audio." },
      { status: 500 },
    );
  }
}
