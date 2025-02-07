type SidebarProps = {
  onFileSelect?: (fileName: string | null) => void;
};

const Sidebar = ({ onFileSelect }: SidebarProps) => {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      onFileSelect?.(file.name);
    }
  };
  return (
    <div className="fixed flex flex-col items-start">
      <input
        id="pdfUpload"
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={handleFileChange}
      />
      <label
        htmlFor="pdfUpload"
        className="cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 mt-4 px-4 rounded"
      >
        Choose PDF
      </label>
    </div>
  );
};

export default Sidebar;
