import { createTheme, MantineColorsTuple } from '@mantine/core';

// Палитра должна идти от самого светлого к самому темному
// Сгенерировано на основе вашего цвета #C8235A
const myCustomPink: MantineColorsTuple = [
    '#ffeef6',
    '#ffdeeb',
    '#fccbd9',
    '#fa9db8',
    '#f7749a',
    '#f55282',
    '#f44075',
    '#d93163',
    '#c22856',
    '#aa1b4a',
];

export const theme = createTheme({
    colors: {
        'custom-pink': myCustomPink,
    },

    primaryColor: 'custom-pink',
    primaryShade: 6,
    fontFamily: "'Raleway', sans-serif",
    defaultRadius: 'md',
});
