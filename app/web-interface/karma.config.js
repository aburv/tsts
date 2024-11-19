module.exports = function(config) {
    config.set({
      browsers: ['ChromeHeadless'],
      customLaunchers: {
        ChromeHeadless: {
          base: 'ChromeHeadless',
          flags: [
            '--no-sandbox',
            '--disable-gpu',
            '--headless',
          ]
        }
      },
      singleRun: true,
      frameworks: ['jasmine'],
      files: [
        // specify the files to be tested here
      ],
      preprocessors: {
        // specify the preprocessors here
      }
    });
  };
  