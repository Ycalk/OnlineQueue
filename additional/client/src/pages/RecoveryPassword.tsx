import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Paper,
    TextInput,
    Button,
    Title,
    Stack,
    Box,
    Text,
} from '@mantine/core';

function RecoveryPass() {
    const [email, setEmail] = useState('');


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
                        <TextInput
                            label="Укажите Email для сброса пароля"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.currentTarget.value)}
                            type="email"
                        />

                        <Button component={Link} to="/notification"
                            fullWidth
                            mt="md"
                            size="md"
                            onClick={recoveryPassword}
                        >
                            Отправить
                        </Button>
                    </Stack>
                </Paper>
            </Box>
        </Box>
    );
}

export default RecoveryPass;
