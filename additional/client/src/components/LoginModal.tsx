import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Modal, TextInput, PasswordInput, Button, Stack, Group, UnstyledButton, Title, Box } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { api } from '../api/ApiClient';

interface LoginModalProps {
    opened: boolean;
    onClose: () => void;
    onSwitchToRegister: () => void;
    onLoginSuccess: () => void;
}

export function LoginModal({ opened, onClose, onSwitchToRegister, onLoginSuccess }: LoginModalProps) {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleAuth = async () => {
        if (!email || !password) {
            notifications.show({ title: 'Ошибка', message: 'Заполните все поля', color: 'red' });
            return;
        }

        setIsLoading(true);
        try {
            const response = await api.request<{ access_token: string }>('/api/v1/auth/login', 'POST', { email, password });
            api.setToken(response.access_token);

            notifications.show({ title: 'Успешно', message: 'Вы вошли в систему', color: 'green' });

            onLoginSuccess();
            onClose();
        } catch (error: any) {
            console.error("Login error:", error);
            notifications.show({ title: 'Ошибка', message: error.message || 'Неверные данные', color: 'red' });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Modal opened={opened} onClose={onClose} title="Вход" centered radius="md">
            <Box style={{ textAlign: 'center', marginBottom: 20 }}>
                <Title order={2} style={{ color: '#e91e63', fontSize: 28 }}>К Телеком</Title>
            </Box>

            <Stack gap="md">
                <TextInput
                    label="Email"
                    placeholder="Введите электронную почту"
                    value={email}
                    onChange={(e) => setEmail(e.currentTarget.value)}
                    disabled={isLoading}
                />
                <PasswordInput
                    label="Пароль"
                    placeholder="Введите пароль"
                    value={password}
                    onChange={(e) => setPassword(e.currentTarget.value)}
                    disabled={isLoading}
                />

                <Group justify="space-between" mt="xs">
                    <UnstyledButton onClick={onSwitchToRegister} size="sm" c="dimmed">Регистрация</UnstyledButton>
                    <UnstyledButton onClick={() => navigate('/password/recovery')} size="sm" c="dimmed">Забыли пароль?</UnstyledButton>
                </Group>

                <Button fullWidth onClick={handleAuth} loading={isLoading} mt="md">
                    Войти
                </Button>
            </Stack>
        </Modal>
    );
}
