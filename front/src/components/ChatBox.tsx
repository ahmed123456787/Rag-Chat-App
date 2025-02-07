import { Send } from "lucide-react";
import { useState, useContext, useEffect } from "react";
import { MessageContext } from "../context/context";
import { useGetReply } from "../hooks/useGetReply";
import ErrorMessage from "./Error";

type ChatBoxProps = {
  fileName?: string | null;
};

function ChatBox({ fileName }: ChatBoxProps) {
  const context = useContext(MessageContext);
  const [message, setMessage] = useState("");
  const { sendMessage, loading, error, setError } = useGetReply(
    context,
    fileName
  );

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSendMessage();
    }
  };

  const handleSendMessage = () => {
    sendMessage(message);
    setMessage("");
  };

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [error, setError]);

  return (
    <div className="fixed bottom-3 left-1/2 transform -translate-x-1/2 w-full max-w-sm md:max-w-md lg:max-w-lg bg-gray-400 p-2 flex flex-col items-start rounded-lg">
      {error && <ErrorMessage message={error} />}

      <div className="flex items-center justify-between w-full">
        <input
          className="outline-none w-full p-1 rounded-l text-sm"
          placeholder="Ask about your document"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyUp={handleKeyPress}
          disabled={loading}
        />

        {loading ? (
          <div className="ml-2 text-sm text-blue-600">Loading...</div>
        ) : (
          <Send
            className="hover:cursor-pointer ml-2 text-sm"
            onClick={handleSendMessage}
          />
        )}
      </div>

      {fileName && (
        <p className="mt-2 text-xs text-slate-800 border border-gray-500 p-1 rounded">
          Current file: {fileName}
        </p>
      )}
    </div>
  );
}

export default ChatBox;
