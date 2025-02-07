import { useContext } from "react";
import { MessageContext } from "../context/context";

const MessageBox = () => {
  const context = useContext(MessageContext);
  return (
    <div className="w-full text-gray-800 p-3 flex flex-col items-end">
      {context?.messages.map((message, index) => (
        <div key={index} className="w-full flex flex-col mb-4">
          <div className="self-end bg-gray-300 p-2 rounded-lg mb-2 max-w-xs">
            <p className="text-sm">{message.message}</p>
          </div>
          <div className="self-start bg-blue-300 p-2 rounded-lg max-w-xs">
            <p className="text-sm">{message.reply}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageBox;
