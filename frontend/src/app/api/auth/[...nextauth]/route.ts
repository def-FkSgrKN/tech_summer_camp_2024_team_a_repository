import NextAuth, { AuthOptions, Session } from "next-auth";
import GitHubProvider from "next-auth/providers/github";
import { JWT } from "next-auth/jwt"; // JWTの型をインポート
import { Account, User } from "next-auth"; // AccountとUserの型をインポート

export const authOptions: AuthOptions = {
  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
  ],
  session: {
    strategy: "jwt" as const,
    maxAge: 30 * 24 * 60 * 60,
  },
  secret: process.env.NEXTAUTH_SECRET,
  callbacks: {
    // JWTの型指定
    async jwt({
      token,
      account,
    }: {
      token: JWT;
      account?: Account | null;
      user?: User | null;
    }): Promise<JWT> {
      if (account) {
        token.accessToken = account.access_token;
      }
      return token;
    },

    async session({
      session,
      token,
    }: {
      session: Session;
      token: JWT;
    }): Promise<Session> {
      session.accessToken = token.accessToken;
      session.user!.id = token.id;
      return session;
    },
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
