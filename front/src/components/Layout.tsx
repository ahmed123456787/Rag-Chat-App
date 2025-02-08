import Sidebar from "./Sidebar";
import ChatBox from "./ChatBox";
import { useState } from "react";

type LayoutProps = {
  children: React.ReactNode;
};

const Layout = ({ children }: LayoutProps) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileSelect = (info: File | null) => {
    setFile(info);
  };
  return (
    <div className="flex w-full bg-gray-200 min-h-screen ">
      <div className="w-1/5 bg-[#2F2A3C] text-gray-100 p-3">
        <Sidebar onFileSelect={handleFileSelect} />
      </div>
      <div className="w-4/5 min-h-screen flex flex-col justify-between">
        <div>{children}</div>
        <div className="p-3 flex items-center justify-center">
          <ChatBox file={file} />
        </div>
      </div>
    </div>
  );
};

export default Layout;
