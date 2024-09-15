"use client";

import { signIn } from "next-auth/react";
import { GithubLoginButton } from "react-social-login-buttons";

export default function AuthPage() {
  const handleSignIn = async () => {
    try {
      const result = await signIn("github");
      if (result?.error) {
        console.error("Sign-in error:", result.error);
      } else {
        console.log("Sign-in successful");
      }
    } catch (error) {
      console.error("Error during sign-in:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl mb-4">Sign in with GitHub</h1>
      <div className="w-96">
        <GithubLoginButton onClick={handleSignIn} />
      </div>
    </div>
  );
}
