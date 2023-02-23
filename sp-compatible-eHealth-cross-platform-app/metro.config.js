module.exports = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: false,
      },
    }),
  },
  resolver: {
    extraNodeModules: {
      stream: require.resolve('readable-stream'),
      'solid-auth-cli': require.resolve('@prodiptapromit/solid-auth-client/lib/index'),
      'solid-auth-client': require.resolve('@prodiptapromit/solid-auth-client/lib/index'),
    },
  },
};
