import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    AppShell,
    Container,
    TextInput,
    Button,
    Card,
    Text,
    Badge,
    Group,
    Title,
    Menu,
    Stack,
    Timeline,
    Textarea,
    SimpleGrid,
    SegmentedControl,
    ScrollArea,
    Box,
    Divider,
} from '@mantine/core';

import {
    IconClipboardText,
    IconSearch,
    IconFriends,
    IconChecklist,
    IconBellRinging,
    IconTransitionLeft,
    IconMenu2,
    IconDownload,
    } from '@tabler/icons-react';

interface HistoryEvent {
    id: number;
    person: string;
    action: string;
    time: string;
}

interface Application {
    id: string;
    title: string;
    status: 'waiting' | 'accepted' | 'rejected' | 'archived';
    statusText: string;
    purpose: string;
    dateTime: string;
    hasAttachment?: boolean;
    history: HistoryEvent[];
}

function MyApplication() {
    const [search, setSearch] = useState('');
    const [activeStatus, setActiveStatus] = useState<string | null>('waiting');
    const [activeTabPerCard, setActiveTabPerCard] = useState<{ [key: string]: 'info' | 'history' }>({});
    const [comments, setComments] = useState<{ [key: string]: string }>({});

    const applications: Application[] = [
        {
        id: '1',
        title: 'Устройство в штаб',
        status: 'waiting',
        statusText: 'В ожидании',
        purpose:
            'Проходил стажировку в сентябре, хочу устроиться на постоянку, если есть такая возможность',
        dateTime: '26/10/2025 14:00 - 16:00',
        hasAttachment: true,
        history: [
            {
            id: 1,
            person: 'Петров Петр Петрович',
            action: 'Добавился в очередь Устройство в штаб',
            time: '3 часа назад',
            },
            {
            id: 2,
            person: 'Иванов Иван Иванович',
            action: 'Утвердил запись на 14:00 часов',
            time: '2 часа назад',
            },
            {
            id: 3,
            person: 'Иванов Иван Иванович',
            action: 'Оставил комментарий: возьмите документы с собой',
            time: '1 час назад',
            },
            {
            id: 4,
            person: 'Петров Петр Петрович',
            action: 'Загрузил дополнительные документы',
            time: '30 минут назад',
            },
            {
            id: 5,
            person: 'Иванов Иван Иванович',
            action: 'Подтвердил получение документов',
            time: '15 минут назад',
            },
        ],
        },
        {
        id: '2',
        title: 'По поводу отпуска',
        status: 'waiting',
        statusText: 'В ожидании',
        purpose: 'Хочу взять отпуск в декабре на две недели',
        dateTime: '27/10/2025 10:00 - 11:00',
        hasAttachment: true,
        history: [
            {
            id: 1,
            person: 'Олегов Олег Олегович',
            action: 'Добавился в очередь По поводу отпуска',
            time: '2 часа назад',
            },
            {
            id: 2,
            person: 'Иванов Иван Иванович',
            action: 'Оставил комментарий: возьмите документы с собой',
            time: '1 час назад',
            },
        ],
        },
        {
        id: '3',
        title: 'Получение премии',
        status: 'accepted',
        statusText: 'Принято',
        purpose: 'Получить премию за сентябрь, согласовано с руководителем',
        dateTime: '30/10/2025 15:00 - 15:30',
        hasAttachment: true,
        history: [
            {
            id: 1,
            person: 'Олегова Екатерина Ильина',
            action: 'Добавилась в очередь Получение премии',
            time: '1 день назад',
            },
            {
            id: 2,
            person: 'Иванов Иван Иванович',
            action: 'Подтвердил выдачу премии',
            time: '3 часа назад',
            },
        ],
        },
        {
        id: '4',
        title: 'Перенос отпуска',
        status: 'rejected',
        statusText: 'Отклонено',
        purpose: 'Хотел перенести отпуск на январь, но нет возможности по графику',
        dateTime: '29/10/2025 11:00 - 11:30',
        hasAttachment: true,
        history: [
            {
            id: 1,
            person: 'Сидоров Алексей Петрович',
            action: 'Подал запрос на перенос отпуска',
            time: '5 часов назад',
            },
            {
            id: 2,
            person: 'Иванов Иван Иванович',
            action: 'Отклонил запрос из-за загруженности отдела',
            time: '2 часа назад',
            },
        ],
        },
    ];

    const filteredApplications = applications.filter((app) => {
        if (activeStatus && app.status !== activeStatus) return false;
        if (search && !app.title.toLowerCase().includes(search.toLowerCase())) return false;
        return true;
    });

    const totalApplications = applications.length;
    const activeApplications = applications.filter(
        (app) => app.status === 'waiting' || app.status === 'accepted'
    ).length;

    const getActiveTab = (appId: string) => activeTabPerCard[appId] || 'info';
    const setActiveTab = (appId: string, tab: 'info' | 'history') => {
        setActiveTabPerCard({ ...activeTabPerCard, [appId]: tab });
    };

    const getComment = (appId: string) => comments[appId] || '';
    const setComment = (appId: string, value: string) => {
        setComments({ ...comments, [appId]: value });
    };

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <AppShell.Header>
                <Container size="100%" h="100%">
                <Group h="100%" px="md" justify="space-between">
                    <Title order={2} c="#e91e63">
                    К Телеком
                    </Title>
                    <Group>
                    <Button variant="outline" color="#b9bbb5ff">
                        Вход
                    </Button>
                    <Button>Регистрация</Button>
                    <Menu shadow="md" width={200}>
                        <Menu.Target>
                        <IconMenu2 size={32} />
                        </Menu.Target>

                        <Menu.Dropdown style={{ zIndex: 1001 }}>
                        <Menu.Item component={Link} to="/" leftSection={<IconClipboardText size={16} />}>
                            Доступные очереди
                        </Menu.Item>
                        <Menu.Item
                            component={Link}
                            to="/my-queue"
                            leftSection={<IconFriends size={16} />}
                        >
                            Мои очереди
                        </Menu.Item>
                        <Menu.Item
                            component={Link}
                            to="/my-application"
                            leftSection={<IconChecklist size={16} />}
                        >
                            Мои заявки
                        </Menu.Item>
                        <Menu.Item leftSection={<IconBellRinging size={16} />}>
                            Настройки уведомлений
                        </Menu.Item>
                        <Menu.Item color="red" leftSection={<IconTransitionLeft size={16} />}>
                            Выход
                        </Menu.Item>
                        </Menu.Dropdown>
                    </Menu>
                    </Group>
                </Group>
                </Container>
        </AppShell.Header>

        <AppShell.Main>
            <Container size="80%" py="md">
                <Title order={1} mb="xs">
                    Мои заявки
                </Title>
                <Group mb="xs">
                    <Text size="sm">
                        Всего заявок: <strong>{totalApplications}</strong>
                    </Text>
                    <Text size="sm">
                        Активных заявок: <strong>{activeApplications}</strong>
                    </Text>
            </Group>

            <Group mb="lg" justify="space-between">
                <Group>
                    <TextInput
                        placeholder="Поиск по названию, имени и т.д."
                        style={{ width: 404 }}
                        value={search}
                        onChange={(e) => setSearch(e.currentTarget.value)}
                    />
                    <Button>
                        <IconSearch size={20} />
                    </Button>
                </Group>

                <SegmentedControl
                    value={activeStatus || 'waiting'}
                    onChange={setActiveStatus}
                    data={[
                        { label: 'Ожидание', value: 'waiting' },
                        { label: 'Принято', value: 'accepted' },
                        { label: 'Отклонено', value: 'rejected' },
                        { label: 'Архивировано', value: 'archived' },
                    ]}
                />
            </Group>
            <Divider size={2} my="sm" />
                <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
                    {filteredApplications.map((app) => (
                        <Card
                            key={app.id}
                            shadow="sm"
                            padding="lg"
                            radius="md"
                            withBorder
                            style={{
                                height: 500,
                                display: 'flex',
                                flexDirection: 'column',
                            }}
                        >
                            <Group justify="space-between" mb="sm">
                                <Title order={4}>{app.title}</Title>
                            </Group>
                            <Group justify="space-between" mb="sm">
                                <Badge
                                color={
                                    app.status === 'waiting'
                                    ? '#C8235A'
                                    : app.status === 'accepted'
                                    ? '#5FBF24'
                                    : app.status === 'rejected'
                                    ? '#FA5252'
                                    : 'gray'
                                }
                                variant="dot"
                                >
                                {app.statusText}
                                </Badge>

                                <Group justify="end">
                                    <SegmentedControl
                                    value={getActiveTab(app.id)}
                                    onChange={(val) => setActiveTab(app.id, val as 'info' | 'history')}
                                    data={[
                                        { label: 'Информация', value: 'info' },
                                        { label: 'История', value: 'history' },
                                    ]}
                                    />
                                </Group>
                            </Group>

                            <Divider size={2} my="sm" />
                            
                            <ScrollArea
                            style={{
                                flex: 1,
                                minHeight: 0,
                            }}
                            type="auto"
                            >
                            <Box pr="xs" pb="xs">
                                {getActiveTab(app.id) === 'info' && (
                                <Stack gap="md">
                                    <div>
                                    <Text size="sm" mb="xs">
                                        <strong>Цель визита:</strong>
                                    </Text>
                                    <Text size="sm" c="gray.7">
                                        {app.purpose}
                                    </Text>
                                    </div>

                                    <div>
                                    <Text size="sm">
                                        <strong>Дата и время посещения:</strong> {app.dateTime}
                                    </Text>
                                    </div>

                                    {app.hasAttachment && (
                                        <Group justify="start" mb="md">
                                            <Button
                                                variant="filled"
                                                leftSection={<IconDownload size={16} />}
                                                size="sm"
                                            >
                                                Скачать приложенный файл
                                            </Button>
                                        </Group>
                                    )}
                                </Stack>
                                )}

                                {getActiveTab(app.id) === 'history' && (
                                <Stack gap="md">
                                    <Timeline active={app.history.length} bulletSize={20} lineWidth={4}>
                                    {app.history.map((item) => (
                                        <Timeline.Item
                                        key={item.id}
                                        title={<Text fw={600}>{item.person}</Text>}
                                        >
                                        <Text c="dimmed" size="xs" mt={4}>
                                            {item.action}
                                        </Text>
                                        <Text size="xs" mt={4} c="gray.5">
                                            {item.time}
                                        </Text>
                                        </Timeline.Item>
                                    ))}
                                    </Timeline>

                                    <Stack gap="sm" mt="md">
                                    <Text size="sm" fw={600}>
                                        Комментарий
                                    </Text>
                                    <Textarea
                                        placeholder="Укажите важные детали или пожелания"
                                        value={getComment(app.id)}
                                        onChange={(e) => setComment(app.id, e.currentTarget.value)}
                                        minRows={3}
                                        size="sm"
                                    />
                                    </Stack>
                                </Stack>
                                )}
                            </Box>
                            </ScrollArea>

                            {app.status === 'waiting' && (
                            <Group grow mt="md">
                                <Button variant="filled" size="sm">
                                Изменить заявку
                                </Button>
                                <Button variant="outline" color="gray" size="sm">
                                Отменить заявку
                                </Button>
                            </Group>
                            )}

                            {app.status === 'accepted' && (
                                <Group justify="end" mb="md">
                                    <Button variant="outline" color="gray" size="sm" mt="md">
                                        Отменить заявку
                                    </Button>
                                </Group>
                            )}
                        </Card>
                    ))}
                </SimpleGrid>
            </Container>
        </AppShell.Main>
    </AppShell>
    );
}

export default MyApplication;
