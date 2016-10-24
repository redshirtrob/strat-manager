import webpack from 'webpack';
import ForceCaseSensitivityPlugin from 'force-case-sensitivity-webpack-plugin';
import baseConfig from './webpack.base.config.js';


module.exports = (opts) => {

  const config = baseConfig(opts);

  return {
    ...config,
    devServer: {
      port: 3000,
      historyApiFallback: true
    },
    plugins: [
      ...config.plugins,
      new ForceCaseSensitivityPlugin(),  // OSX wont check but other unix os will
      new webpack.NoErrorsPlugin(),
    ],
  };
};
