import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Paper,
    TextInput,
    Button,
    Title,
    Stack,
    Box,
    Text
} from '@mantine/core';

function RecoveryPass() {
    const [email, setEmail] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);

    const recoveryPassword = () => {
        console.log("Отправка письма на:", email);
        setIsSubmitted(true);
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

                    {isSubmitted ? (
                        <Stack gap="md" align="center">
                            <Text size="lg" fw={500} ta="center">Проверьте почту</Text>
                            <Text ta="center" c="dimmed">
                                Ссылка для восстановления пароля была отправлена на <b>{email}</b>.
                            </Text>

                            <Button
                                component={Link}
                                to="/"
                                fullWidth
                                mt="md"
                                variant="outline"
                            >
                                Вернуться на главную
                            </Button>
                        </Stack>
                    ) : (
                        <Stack gap="md">
                            <Text size="lg" fw={500} ta="center">Восстановление пароля</Text>
                            <Text size="sm" c="dimmed" ta="center">
                                Введите ваш email, и мы отправим вам инструкции по сбросу пароля.
                            </Text>

                            <TextInput
                                label="Email"
                                placeholder="Введите электронную почту"
                                value={email}
                                onChange={(e) => setEmail(e.currentTarget.value)}
                                type="email"
                                required
                            />

                            <Button
                                fullWidth
                                mt="md"
                                size="md"
                                onClick={recoveryPassword}
                                disabled={!email}
                            >
                                Отправить
                            </Button>

                            <Button
                                component={Link}
                                to="/?action=login"
                                variant="subtle"
                                size="sm"
                                c="dimmed"
                            >
                                Отмена
                            </Button>
                        </Stack>
                    )}
                </Paper>
            </Box>
        </Box>
    );
}

export default RecoveryPass;
