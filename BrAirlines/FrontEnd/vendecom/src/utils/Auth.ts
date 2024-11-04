// auth.ts
export const isUserLoggedIn = (): boolean => {
    const token = localStorage.getItem("token");
    return token !== null && token !== "";
  };
  export const logout = (): void => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

  };

  