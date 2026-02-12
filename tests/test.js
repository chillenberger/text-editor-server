
const PLANNING_API_URL = "http://localhost:8000/plan/invoke";

async function toolFileSystem() {
  return `{
      "folder1": {
        "file1.txt": {},
        "file2.txt": {},
      },
      "folder2": {
        "file3.txt": {},
        "file4.txt": {},
      },
    }`
}

async function toolRenameFile(oldPath, newPath) {
  return `Renamed ${oldPath} to ${newPath}`
}



export class PlanningService {
  async executePlanningLoop(newMessage) {
    const responses = [];

    const messages = [];
    while (true) {
      try {
        const parsedResponse = await this.invokePlan(messages, newMessage);
        const output = parsedResponse.output;
        messages.push(...[newMessage, output]);

        console.log("output: ", output);

        if (output.type === "end" || output.type === "message") {
          // Planning complete
          break;
        }

        if (output.type === "tool_call" && output.tool) {
          const toolCall = output.tool;
          const result = await this.executeTool(toolCall.name, toolCall.args);
          newMessage = toolMessage(JSON.stringify(result), toolCall.id, toolCall.name);
          continue;
        }
      } catch (error) {
        throw new Error(
          `Error during planning loop: ${error instanceof Error ? error.message : "Unknown error"}`
        );
      }
    }

    return responses;
  }


  async executeTool(toolName, args) {
    switch (toolName) {
      case "get_workspace_structure":
        return toolFileSystem();
      case "rename_file":
        return toolRenameFile(args.old_path, args.new_path);
      default:
        throw new Error(`Unknown tool ${toolName}`);
    }
  }

  async invokePlan(messages, newMessage) {
    try {
      const response = await fetch(PLANNING_API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(
          {
            input: {
              messages: messages,
              new_message: newMessage
            }
          })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(
        `Error during planning loop: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
}

function humanMessage(content) {
  return {
    type: "human",
    content,
  }
}

function assistantMessage(content) {
  return {
    type: "assistant",
    content,
  }
}

function toolMessage(content, toolCallId, toolName) {
  return {
    type: "tool",
    content: content,
    tool_call_id: toolCallId,
    tool_name: toolName,
  }
}


function main() {
  const instruction = humanMessage("Rename file1.txt to file1-renamed.txt");

  const planningService = new PlanningService();
  const responses = planningService.executePlanningLoop(instruction);
  console.log(responses);
}

main();