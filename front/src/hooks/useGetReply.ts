import { useState } from "react";
import axios from "axios";

export function useGetReply(context: any, fileName?: string | null) {
  const apiUrl = "http://localhost:8000";

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (message: string) => {
    if (!fileName) {
      setError("Please select a file first.");
      return;
    }
    if (!context || message.trim() === "") return;

    setLoading(true);

    try {
      const response = await axios.get(`${apiUrl}/test/`, {
        // message,
      });
      context.addMessage({ message, reply: response.data.message });
    } catch (err) {
      setError("Failed to fetch response. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return { sendMessage, loading, error, setError };
}
