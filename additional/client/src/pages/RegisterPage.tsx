import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { notifications } from '@mantine/notifications';
import {
    Paper,
    TextInput,
    PasswordInput,
    Button,
    Title,
    Stack,
    Box,
} from '@mantine/core';
import { api } from '../api/ApiClient';

function RegisterPage() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [patronymic, setPatronymic] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleRegister = async () => {
        if (!email || !password || !firstName || !lastName) {
            notifications.show({
                title: 'Ошибка',
                message: 'Заполните обязательные поля',
                color: 'red',
            });
            return;
        }

        if (password !== confirmPassword) {
            notifications.show({
                title: 'Ошибка',
                message: 'Пароли не совпадают',
                color: 'red',
            });
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

            notifications.show({
                title: 'Успешно',
                message: 'Вы успешно зарегистрировались!',
                color: 'green',
            });

            navigate('/');

        } catch (error: any) {
            console.error("Registration error:", error);
            notifications.show({
                title: 'Ошибка регистрации',
                message: error.message || 'Что-то пошло не так',
                color: 'red',
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
                backgroundColor: '#f5f5f5',
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
                            label="Имя"
                            placeholder="Введите ваше имя"
                            required
                            value={firstName}
                            onChange={(e) => setFirstName(e.currentTarget.value)}
                            disabled={isLoading}
                        />

                        <TextInput
                            label="Фамилия"
                            placeholder="Введите вашу фамилию"
                            required
                            value={lastName}
                            onChange={(e) => setLastName(e.currentTarget.value)}
                            disabled={isLoading}
                        />

                        <TextInput
                            label="Отчество"
                            placeholder="Введите ваше отчество"
                            value={patronymic}
                            onChange={(e) => setPatronymic(e.currentTarget.value)}
                            disabled={isLoading}
                        />

                        <TextInput
                            label="Email"
                            placeholder="Введите электронную почту"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.currentTarget.value)}
                            type="email"
                            disabled={isLoading}
                        />

                        <PasswordInput
                            label="Пароль"
                            placeholder="Введите пароль"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.currentTarget.value)}
                            disabled={isLoading}
                        />

                        <PasswordInput
                            label="Повторите пароль"
                            placeholder="Введите пароль ещё раз"
                            required
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.currentTarget.value)}
                            disabled={isLoading}
                            error={confirmPassword && password !== confirmPassword ? 'Пароли не совпадают' : null}
                        />

                        <Button
                            fullWidth
                            mt="md"
                            size="md"
                            onClick={handleRegister}
                            loading={isLoading}
                        >
                            Зарегистрироваться
                        </Button>
                    </Stack>
                </Paper>
            </Box>
        </Box>
    );
}

export default RegisterPage;
