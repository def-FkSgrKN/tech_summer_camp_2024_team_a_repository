"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const Home = () => {
  const [isStarted, setIsStarted] = useState(false);
  const handeClick = () => {
    setIsStarted(true);
  };

  const router = useRouter();

  return (
    <div className="bg-neutral-600 min-h-screen flex flex-col">
      <div className="flex justify-center mt-10">
        <h1 className="text-center text-green-500 text-5xl">Your Name</h1>
      </div>
      {isStarted ? (
        <div className="mx-auto max-w-xl mt-32 flex-grow">ビデオを入れる</div>
      ) : (
        <button
          className="btn btn-blue mx-auto mt-20 mb-10 bg-green-700 hover:bg-blue-700 text-white font-bold text-xl py-4 px-8 rounded-full"
          onClick={handeClick}
        >
          Start
        </button>
      )}
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
};

export default Home;
