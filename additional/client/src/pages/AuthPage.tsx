import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
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
import { notifications } from '@mantine/notifications';
import { api } from '../api/ApiClient';

function AuthPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleAuth = async () => {
        if (!email || !password) {
             notifications.show({
                title: 'Ошибка валидации',
                message: 'Пожалуйста, заполните все поля',
                color: 'red',
            });
            return;
        }

        setIsLoading(true);

        try {
            const response = await api.request<{ access_token: string }>('/api/v1/auth/login', 'POST', {
                email,
                password
            });
            
            api.setToken(response.access_token);
            
            navigate('/'); 
        } catch (error: any) {
            console.error("Ошибка входа:", error);
            
            notifications.show({
                title: 'Ошибка входа',
                message: error.message || 'Неверный логин или пароль',
                color: 'red',
                autoClose: 5000,
            });
        } finally {
            setIsLoading(false);
        }
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
                            disabled={isLoading}
                        />

                        <PasswordInput
                            placeholder="Пароль"
                            value={password}
                            onChange={(e) => setPassword(e.currentTarget.value)}
                            disabled={isLoading}
                        />

                        <Group justify="end">
                            <UnstyledButton component={Link} to="/recovery-password">Забыли пароль?</UnstyledButton>
                        </Group>

                        <Button 
                            fullWidth
                            mt="md"
                            size="md"
                            onClick={handleAuth}
                            loading={isLoading}
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
