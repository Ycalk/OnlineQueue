import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Paper,
    PasswordInput,
    Button,
    Title,
    Stack,
    Box,
    Text,
} from '@mantine/core';

function NewPass() {
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const recoveryPassword = () => {
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
                        <Text>Восстановление пароля</Text>
                        <PasswordInput
                            placeholder="Новый пароль"
                            value={password}
                            onChange={(e) => setPassword(e.currentTarget.value)}
                        />
                        
                        <PasswordInput
                            placeholder="Введите пароль ещё раз"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.currentTarget.value)}
                        />

                        <Button component={Link} to="/return"
                            fullWidth
                            mt="md"
                            size="md"
                            onClick={recoveryPassword}
                        >
                            Сохранить
                        </Button>
                    </Stack>
                </Paper>
            </Box>
        </Box>
    );
}

export default NewPass;
