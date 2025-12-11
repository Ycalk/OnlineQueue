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
} from '@mantine/core';

function RegisterPage() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [patronymic, setPatronymic] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleRegister = () => {
        // Здесь будет логика регистрации
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
                        />

                        <TextInput
                            label="Фамилия"
                            placeholder="Введите вашу фамилию"
                            required
                            value={lastName}
                            onChange={(e) => setLastName(e.currentTarget.value)}
                        />

                        <TextInput
                            label="Отчество"
                            placeholder="Введите ваше отчество"
                            required
                            value={patronymic}
                            onChange={(e) => setPatronymic(e.currentTarget.value)}
                        />

                        <TextInput
                            label="Email"
                            placeholder="Введите электронную почту"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.currentTarget.value)}
                            type="email"
                        />

                        <PasswordInput
                            label="Пароль"
                            placeholder="Введите пароль"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.currentTarget.value)}
                        />

                        <PasswordInput
                            label="Повторите пароль"
                            placeholder="Введите пароль ещё раз"
                            required
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.currentTarget.value)}
                        />

                        <Button component={Link} to="/"
                            fullWidth
                            mt="md"
                            size="md"
                            onClick={handleRegister}
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
