## Prompt for LLM

System Prompt/Instruction:

```yaml
You are a technical book editor, and doing the following task:

This is a {transcript} from a video {title} belong to a {topic}, let split the {transcripts} into multiple semantic sections to express idea as much detail as possible, each section may contain multiple paragraphs; precisely separate the sections by a blank line.

Generate a short summary line or topic line for each session and make the summary line in Bold text, place the summary line at the beginning of each section.

KEEP all the words from the {transcripts}, can add new words for the summary line. An empty line between each section or each paragraph or summary line.

Output: Markdown format. Remove the {title} or {topic} from the output, remove all heading line. Remove all the HTML tag. Use simple ASCII standard for text punctuation.
```

Prompt Structure:

```yaml
topic: {course.title}, {module.title}; title: {activity.title}; transcript: {activity.transcript}
```

Sample Prompt:

```yaml
topic: "Conversational AI on Vertex AI and Dialogflow CX, Vertex AI Search and Conversation Architecture and Security"; title: "Data governance and compliance"; transcript: "in this lesson you'll learn more about data governance and compliance with Google Cloud Google Cloud products Empower Enterprises to embrace generative AI with the confidence that there is data governance built in this is especially important and highly regulated Industries like financial services and Healthcare where you need to guarantee that no one can access confidential or sensitive data you also want to be certain that none of your data or your customers data is being used for any other purpose than determined by you so let's outline Google Cloud's approach to governance of customer data for cloud llms and generative AI Google cloud is always committed to transparency compliance with regulations like gdpr and HIPAA and privacy best practices by default Google Cloud does not use customer data to train llms in accordance with the Google Cloud terms and the cloud data processing addendum and Google Cloud will obtain customer permission before using any customer data to train llms"
```

Generated Prompt Sample:

- [Conversational AI on Vertex AI and Dialogflow CX](docs/samples/data/courses/892-prompt.json)

```json
{
  "id": "892",
  "title": "Conversational AI on Vertex AI and Dialogflow CX",
  "modules": {
    "Course Introduction": {
      "432841": {
        "425551": {
          "title": "Course Introduction",
          "transcript": "topic: Conversational AI on Vertex AI and Dialogflow CX, Course Introduction; title: Course Introduction; transcript: Welcome to the course Conversational AI on Vertex AI and Dialogflow CX. This course is intended for developers and conversational designers. Please be aware that this course content builds upon concepts taught in the course: Customer Experiences with Contact Center AI. You can find this course in Cloud Skills Boost. If you haven't already, please review that course and then come back to learn the new capabilities that generative AI and conversational AI is bringing to CCAI and Dialogflow CX. If you are familiar with Dialogflow CX, but need a refresher, there's a short review in this module. It is also helpful if you have a good understanding of the fundamentals of Google Cloud, there is also a course on this in Cloud Skills Boost. In this course, you'll learn: [...] About Vertex AI Conversation, a single powerful platform for building conversational AI solutions that use Generative AI, and the key benefits of using Vertex AI Conversation features in Dialogflow CX. Dialogflow CX, is now supercharged with generative AI features. The core components of these new features are generative AI Agents, Data Stores, Generators and Generative Fallback. You'll explore how the new generative AI features help virtual agents handle specific customer interactions. And, where in your current Dialogflow CX solution, these generative features can be integrated. You'll learn about Generators and the various capabilities that they can bring to your Dialogflow CX agents. Generators can be customized and configured to generate dynamic responses or text that can be used during fulfillment. And you'll explore examples of how to write prompts to generate various responses for your customers. And, you'll find out how to configure and deploy generators in your Dialogflow CX solution. You'll learn how Generative Fallback is a mechanism for handling points in the user conversation where the the conversation moves away from the intended flow. And, how the quality of your virtual agents interactions can be enhanced by more natural and conversational responses. You'll discover that you can enable generative fallback on no-match event handlers, which can be used at three levels: in flows, pages, or during parameter filling. And you'll learn how to configure and enable generative fallback at all the necessary levels of you Dialogflow CX solution. Finally, you'll learn more about Generative AI Agents, hybrid agents and data stores. Including when to use intent-based flows, generative AI, or a mix of intents-based flows and generative AI for certain use cases. You'll explore the two methods for enabling generative AI features for your virtual agent, either by creating a generative AI agent, or by adding generative capabilities to your existing agent with data store handlers. And you'll look at the costs of enabling Conversational AI in your Dialogflow CX solution, for both standard and enterprise customers."
        }
      },
      ...
    }
  }
}
```
