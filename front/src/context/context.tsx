import { createContext, useState, ReactNode } from "react";

type MessageType = {
  message: string;
  reply: string;
};

type MessageContextType = {
  messages: MessageType[];
  addMessage: (msg: MessageType) => void;
};

export const MessageContext = createContext<MessageContextType | undefined>(
  undefined
);

type MessageProviderProps = {
  children: ReactNode;
};

export const MessageProvider = ({ children }: MessageProviderProps) => {
  const [messages, setMessages] = useState<MessageType[]>([]);

  const addMessage = (msg: MessageType) => {
    setMessages((prevMessages) => [...prevMessages, msg]);
  };

  return (
    <MessageContext.Provider value={{ messages, addMessage }}>
      {children}
    </MessageContext.Provider>
  );
};
