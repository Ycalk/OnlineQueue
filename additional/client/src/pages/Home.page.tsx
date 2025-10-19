import { useState } from 'react';
import {
    AppShell,
    Container,
    TextInput,
    Button,
    Card,
    Text,
    Badge,
    Group,
    SimpleGrid,
    Title,
} from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';

interface Queue {
    id: string;
    title: string;
    owner: string;
    closestWindow: string;
    duration: string;
    status: 'active' | 'inactive';
}

function HomePage() {
    const [search, setSearch] = useState('');

    const queues: Queue[] = [
        {
            id: '1',
            title: 'Вопросы по поводу отпуска',
            owner: 'Иванов Иван Иванович',
            closestWindow: '10:00',
            duration: '15 минут',
            status: 'active'
        },
        {
            id: '2',
            title: 'Вопросы по больничному',
            owner: 'Иванов Иван Иванович',
            closestWindow: '16:00',
            duration: '10 минут',
            status: 'active'
        },
        {
            id: '3',
            title: 'Устройство в штаб',
            owner: 'Степанов Степан Степанович',
            closestWindow: 'нет',
            duration: '15 минут',
            status: 'inactive'
        },
        {
            id: '4',
            title: 'Субботник',
            owner: 'Иванов Иван Иванович',
            closestWindow: 'нет',
            duration: '15 минут',
            status: 'inactive'
        },
        {
            id: '5',
            title: 'Получение премии',
            owner: 'Иванов Иван Иванович',
            closestWindow: 'нет',
            duration: '15 минут',
            status: 'inactive'
        },
        {
            id: '6',
            title: 'Стажировка',
            owner: 'Иванов Иван Иванович',
            closestWindow: 'нет',
            duration: '15 минут',
            status: 'inactive'
        }
    ];

    return (
        <AppShell
            header={{ height: 70 }}
            padding="md"
        >
            <AppShell.Header>
                <Container size="xl" h="100%">
                    <Group h="100%" px="md" justify="space-between">
                        <Title order={2} c="#e91e63">К Телеком</Title>
                        <Group>
                            <Button variant="subtle">Вход</Button>
                            <Button>Регистрация</Button>
                        </Group>
                    </Group>
                </Container>
            </AppShell.Header>

            <AppShell.Main>
                <Container size="xl" py="xl">
                    <Title order={1} mb="xl">Доступные очереди</Title>

                    <Group mb="xl" justify="space-between">
                        <TextInput
                            placeholder="Поиск по названию, имени и т.д."
                            leftSection={<IconSearch size={16} />}
                            style={{ flex: 1, maxWidth: 400 }}
                            value={search}
                            onChange={(e) => setSearch(e.currentTarget.value)}
                        />
                        <Button leftSection={<span>+</span>}>
                            Создать очередь
                        </Button>
                    </Group>

                    <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
                        {queues.map((queue) => (
                            <Card key={queue.id} shadow="sm" padding="lg" radius="md" withBorder>
                                <Title order={4} mb="md">{queue.title}</Title>

                                <Text size="sm" mb={4}>
                                    Владелец: {queue.owner}
                                </Text>
                                <Text size="sm" mb={4}>
                                    Ближайшее окно: {queue.closestWindow}
                                </Text>
                                <Text size="sm" mb="lg">
                                    Длительность: {queue.duration}
                                </Text>
                                <Group justify="space-between" align="center">
                                    <Badge
                                        color={queue.status === 'active' ? 'green' : 'gray'}
                                        variant="dot"
                                    >
                                        {queue.status === 'active' ? 'Активна' : 'Неактивна'}
                                    </Badge>
                                    <Button size="sm">
                                        Открыть
                                    </Button>
                                </Group>
                            </Card>
                        ))}
                    </SimpleGrid>
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}

export default HomePage;