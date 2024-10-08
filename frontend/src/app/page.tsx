import { getServerSession } from "next-auth";
import { authOptions } from "./api/auth/[...nextauth]/route";
import CameraPage from "./components/camera";

export default async function Home() {
  const session = await getServerSession(authOptions);

  return (
    <div className="bg-neutral-600 min-h-screen flex flex-col">
      <div className="flex justify-center mt-6">
        <h1 className="text-center text-green-500 text-5xl">Fuuma</h1>
      </div>
      <div className="mx-auto max-w-lg mt-10 flex-grow">
        <CameraPage session={session} />{" "}
        {/* セッションをクライアントコンポーネントに渡す */}
      </div>
      <div className="mt-20 mx-auto max-w-xl mb-10">
        <h2 className="text-center text-green-500">データ</h2>
        <ul className="text-center mt-6 space-y-4 text-green-500">
          <li>過去のデータが入ります</li>
          <li>過去のデータが入ります</li>
          <li>過去のデータが入ります</li>
        </ul>
      </div>
    </div>
  );
}
