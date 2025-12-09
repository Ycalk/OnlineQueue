import { Link } from 'react-router-dom';
import {
    Paper,
    Title,
    Stack,
    Box,
    Text,
    Button,
} from '@mantine/core';

function ReturnToEnter() {

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
                        <Text>Пароль успешно обновлен</Text>

                        <Button component={Link} to="/authorisation"
                            fullWidth
                            mt="md"
                            size="md"
                        >
                            Вернуться ко входу
                        </Button>
                    </Stack>
                </Paper>
            </Box>
        </Box>
    );
}

export default ReturnToEnter;
