module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest'
  },
  //setupFiles: ['./setupTests.js'], // Ensure the path is correct
  collectCoverage: true,
  collectCoverageFrom: ['src/**/*.{js,vue}', '!src/main.js'],
  coverageReporters: ['lcov', 'text-summary'],
  testEnvironmentOptions: {
    customExportConditions: ["node", "node-addons"]
  }
}