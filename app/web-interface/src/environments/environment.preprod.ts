export const environment = {
  production: true,
  authKey: (window as any)['env']['AUTH_KEY'],
  googleServiceAccount: (window as any)['env']['G_CLIENT_ID'],
  separator:(window as any)['env']['SEPARATOR']
};
