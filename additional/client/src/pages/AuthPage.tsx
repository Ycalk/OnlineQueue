import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Paper,
    TextInput,
    PasswordInput,
    Button,
    Title,
    Stack,
    Box,
    UnstyledButton,
    Group,
} from '@mantine/core';

function AuthPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');


    const handleAuth = () => {
        // Здесь будет логика входа
    };

    return (
        <Box
            style={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            <Box style={{ width: '372px', maxWidth: '90%' }}>
                <Paper withBorder shadow="md" p={30} mt={30} radius="md">
                    <Box style={{ textAlign: 'center', marginBottom: 30 }}>
                        <Title
                            order={2}
                            style={{
                                color: '#e91e63',
                                fontWeight: 700,
                                fontSize: 28,
                            }}
                        >
                            К Телеком
                        </Title>
                    </Box>

                    <Stack gap="md">
                        <TextInput
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.currentTarget.value)}
                            type="email"
                        />

                        <PasswordInput
                            placeholder="Пароль"
                            value={password}
                            onChange={(e) => setPassword(e.currentTarget.value)}
                        />

                        <Group justify="end">
                            <UnstyledButton component={Link} to="/recovery-password">Забыли пароль?</UnstyledButton>
                        </Group>

                        <Button component={Link} to="/"
                            fullWidth
                            mt="md"
                            size="md"
                            onClick={handleAuth}
                        >
                            Войти
                        </Button>
                    </Stack>
                </Paper>
            </Box>
        </Box>
    );
}

export default AuthPage;
