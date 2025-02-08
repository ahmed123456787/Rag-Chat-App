import { useState } from "react";
import axios from "axios";

export function useGetReply(context: any, fileName?: File | null) {
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
      // Create FormData and append the file
      const formData = new FormData();
      formData.append("file", fileName);
      formData.append("message", message);

      const response = await axios.post(`${apiUrl}/document/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log(response.data);
      context.addMessage({ message, reply: response.data.message });
    } catch (err) {
      setError("Failed to fetch response. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return { sendMessage, loading, error, setError };
}
