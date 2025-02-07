type ErrorMessageProps = {
  message: string;
};

const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 bg-red-500 text-white p-2 rounded-2xl shadow-lg">
      {message}
    </div>
  );
};

export default ErrorMessage;
