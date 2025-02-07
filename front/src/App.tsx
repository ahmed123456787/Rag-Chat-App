import Layout from "./components/Layout";
import { MessageProvider } from "./context/context";
import MessageBox from "./components/Message";

function App() {
  return (
    <MessageProvider>
      <Layout>
        <div className=" text-gray-800 p-6">
          <MessageBox />
        </div>
      </Layout>
    </MessageProvider>
  );
}

export default App;
