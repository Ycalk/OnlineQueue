import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import './index.css';

import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { ModalsProvider } from '@mantine/modals'
import { Router } from './Router';
import { theme } from './theme';
import { AuthProvider } from './context/AuthContext';

export default function App() {
    return (
        <MantineProvider forceColorScheme="light" theme={theme}>
            <ModalsProvider>
                <AuthProvider>
                    <Notifications />
                    <Router />
                </AuthProvider>
            </ModalsProvider>
        </MantineProvider>
    );
}
