import { useState } from 'react';
import { Modal, TextInput, PasswordInput, Button, Stack, Title, Box } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { api } from '../api/ApiClient';

interface RegisterModalProps {
    opened: boolean;
    onClose: () => void;
    onRegisterSuccess: () => void;
}

export function RegisterModal({ opened, onClose, onRegisterSuccess }: RegisterModalProps) {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [patronymic, setPatronymic] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleRegister = async () => {
        if (!email || !password || !firstName || !lastName) {
            notifications.show({ title: 'Ошибка', message: 'Заполните обязательные поля', color: 'red' });
            return;
        }
        if (password !== confirmPassword) {
            notifications.show({ title: 'Ошибка', message: 'Пароли не совпадают', color: 'red' });
            return;
        }

        setIsLoading(true);
        try {
            const requestData = {
                email,
                password,
                first_name: firstName,
                last_name: lastName,
                patronymic: patronymic.trim() === '' ? null : patronymic,
            };

            const response = await api.request<{ access_token: string }>('/api/v1/auth/register', 'POST', requestData);
            api.setToken(response.access_token);

            notifications.show({ title: 'Успешно', message: 'Регистрация прошла успешно', color: 'green' });

            onRegisterSuccess();
            onClose();
        } catch (error: any) {
            notifications.show({ title: 'Ошибка', message: error.message || 'Ошибка регистрации', color: 'red' });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Modal opened={opened} onClose={onClose} title="Регистрация" centered radius="md">
            <Box style={{ textAlign: 'center', marginBottom: 20 }}>
                <Title order={2} style={{ color: '#e91e63', fontSize: 28 }}>К Телеком</Title>
            </Box>

            <Stack gap="md">
                <TextInput label="Имя" placeholder="Введите ваше имя" required value={firstName} onChange={(e) => setFirstName(e.currentTarget.value)} disabled={isLoading} />
                <TextInput label="Фамилия" placeholder="Введите вашу фамилию" required value={lastName} onChange={(e) => setLastName(e.currentTarget.value)} disabled={isLoading} />
                <TextInput label="Отчество" placeholder="Введите ваше отчество" value={patronymic} onChange={(e) => setPatronymic(e.currentTarget.value)} disabled={isLoading} />
                <TextInput label="Email" placeholder="Введите электронную почту" required value={email} onChange={(e) => setEmail(e.currentTarget.value)} disabled={isLoading} />
                <PasswordInput label="Пароль" placeholder="Введите пароль" required value={password} onChange={(e) => setPassword(e.currentTarget.value)} disabled={isLoading} />
                <PasswordInput
                    label="Повторите пароль"
                    placeholder="Введите пароль повторно"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.currentTarget.value)}
                    disabled={isLoading}
                    error={confirmPassword && password !== confirmPassword ? 'Пароли не совпадают' : null}
                />

                <Button fullWidth onClick={handleRegister} loading={isLoading} mt="md">
                    Зарегистрироваться
                </Button>
            </Stack>
        </Modal>
    );
}
