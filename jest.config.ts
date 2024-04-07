/* eslint-disable */
export default {
  displayName: 'py-tg-bot-weather-agent',
  preset: '../../jest.preset.js',
  testEnvironment: 'node',
  transform: {
    '^.+\\.[tj]s$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.spec.json' }],
  },
  moduleFileExtensions: ['ts', 'js', 'html', 'py'],
  coverageDirectory: '../../coverage/apps/py-tg-bot-weather-agent',
};
