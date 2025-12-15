import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
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
    Menu,
    Paper,
    Box,
    ScrollArea,
    Stack,
    Textarea,
    ActionIcon,
    Divider,
    NumberInput,
    Avatar,
    Loader
} from '@mantine/core';

import {
    IconClipboardText,
    IconSearch,
    IconFriends,
    IconChecklist,
    IconBellRinging,
    IconTransitionLeft,
    IconMenu2,
    IconPlus,
} from '@tabler/icons-react';
import { api } from '../api/ApiClient';

// Тип данных пользователя с бэкенда
interface UserProfile {
    email: string;
    first_name: string;
    last_name: string;
    patronymic: string;
}

interface Queue {
    id: string;
    title: string;
    owner: string;
    closestWindow: string;
    duration: string;
    status: 'active' | 'inactive';
    description?: string;
    email?: string;
    phone?: string;
    fullPurpose?: string;
    startTime?: string;
    endTime?: string;
}

function HomePage() {
    const navigate = useNavigate();

    // Состояние авторизации и данные пользователя
    const [user, setUser] = useState<UserProfile | null>(null);
    const [isAuthLoading, setIsAuthLoading] = useState(true); // Чтобы не мигал интерфейс при загрузке

    const [search, setSearch] = useState('');
    const [selectedQueue, setSelectedQueue] = useState<Queue | null>(null);
    const [showCreateQueue, setShowCreateQueue] = useState(false);

    // Поля формы записи
    const [appointmentDate, setAppointmentDate] = useState('');
    const [appointmentTime, setAppointmentTime] = useState('');
    const [visitPurpose, setVisitPurpose] = useState('');

    // Поля формы создания очереди
    const [queueName, setQueueName] = useState('');
    const [queueDescription, setQueueDescription] = useState('');
    const [queueAutocloseDays, setQueueAutocloseDays] = useState('7');
    const [queueStartTime, setQueueStartTime] = useState('');
    const [queueEndTime, setQueueEndTime] = useState('');

    // Проверка авторизации и получение данных пользователя
    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) {
                setIsAuthLoading(false);
                return;
            }

            try {
                const userData = await api.request<UserProfile>('/api/v1/users/me');
                setUser(userData);
            } catch (error) {
                console.error("Failed to fetch user profile", error);
                api.clearToken(); // Если токен невалиден, чистим его
                setUser(null);
            } finally {
                setIsAuthLoading(false);
            }
        };

        fetchUser();
    }, []);

    const handleLogout = async () => {
        try {
            await api.request('/api/v1/auth/logout', 'POST');
        } catch (error) {
            console.error("Logout error", error);
        } finally {
            api.clearToken();
            setUser(null);
            navigate('/');
        }
    };

    const queues: Queue[] = [
        {
            id: '1',
            title: 'Вопросы по поводу отпуска',
            owner: 'Иванов Иван Иванович',
            closestWindow: '10:00',
            duration: '15 минут',
            status: 'active',
            description: 'Любые возможные вопросы по поводу отпуска на ближайшие полгода',
            email: 'ivanov@example.com',
            phone: '+7 900 000 11 11',
            fullPurpose: 'Любые возможные вопросы по поводу отпуска на ближайшие полгода',
            startTime: '10:00',
            endTime: '12:00',
        },
        // ... (остальные очереди оставлены без изменений для краткости)
        {
            id: '2',
            title: 'Вопросы по больничному',
            owner: 'Иванов Иван Иванович',
            closestWindow: '16:00',
            duration: '10 минут',
            status: 'active',
            description: 'Вопросы по оформлению больничного листа',
            email: 'ivanov@example.com',
            phone: '+7 900 000 11 11',
            fullPurpose: 'Вопросы по оформлению больничного листа',
            startTime: '16:00',
            endTime: '17:00',
        },
    ];

    const handleOpenQueue = (queue: Queue) => {
        setSelectedQueue(queue);
        setAppointmentDate('');
        setAppointmentTime(queue.closestWindow !== 'нет' ? queue.closestWindow : '');
        setVisitPurpose(queue.description || '');
    };

    const handleClosePanel = () => {
        setSelectedQueue(null);
    };

    const handleCloseCreatePanel = () => {
        setShowCreateQueue(false);
        setQueueName('');
        setQueueDescription('');
        setQueueAutocloseDays('7');
        setQueueStartTime('');
        setQueueEndTime('');
    };

    const handleCreateQueue = () => {
        if (!user) {
            navigate('/authorization');
            return;
        }
        handleCloseCreatePanel();
    };

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <AppShell.Header>
                <Container size="100%" h="100%">
                    <Group h="100%" px="md" justify="space-between">
                        <Title order={2} c="#e91e63">К Телеком</Title>

                        <Group>
                            {isAuthLoading ? (
                                <Loader size="sm" color="gray" />
                            ) : !user ? (
                                <>
                                    <Button component={Link} to="/authorization" variant="outline" color='#b9bbb5ff'>
                                        Вход
                                    </Button>
                                    <Button component={Link} to="/registration">
                                        Регистрация
                                    </Button>
                                </>
                            ) : (
                                <Group gap="xs">
                                    {/* Отображаем почту пользователя */}
                                    <Text size="sm" fw={500} mr="xs">
                                        {user.email}
                                    </Text>

                                    <Menu shadow="md" width={200} position="bottom-end">
                                        <Menu.Target>
                                            <ActionIcon variant="transparent" size="xl" color="black">
                                                <IconMenu2 size={32} />
                                            </ActionIcon>
                                        </Menu.Target>

                                        <Menu.Dropdown style={{ zIndex: 1001 }}>
                                            <Menu.Item component={Link} to="/" leftSection={<IconClipboardText size={16} />}>
                                                Доступные очереди
                                            </Menu.Item>
                                            <Menu.Item component={Link} to="/my-queue" leftSection={<IconFriends size={16} />}>
                                                Мои очереди
                                            </Menu.Item>
                                            <Menu.Item component={Link} to="/my-application" leftSection={<IconChecklist size={16} />}>
                                                Мои заявки
                                            </Menu.Item>
                                            <Menu.Item leftSection={<IconBellRinging size={16} />}>
                                                Настройки уведомлений
                                            </Menu.Item>
                                            <Menu.Divider />
                                            <Menu.Item
                                                color="red"
                                                leftSection={<IconTransitionLeft size={16} />}
                                                onClick={handleLogout}
                                            >
                                                Выход
                                            </Menu.Item>
                                        </Menu.Dropdown>
                                    </Menu>
                                </Group>
                            )}
                        </Group>
                    </Group>
                </Container>
            </AppShell.Header>

            <AppShell.Main>
                <Container size="80%" py="md">
                    <Title order={1} mb="lg">Доступные очереди</Title>

                    <Group mb="lg" justify='space-between'>
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
                        {/* Кнопка создания доступна только авторизованным */}
                        {user && (
                            <Button leftSection={<IconPlus size={16} />} onClick={() => setShowCreateQueue(true)}>
                                Создать очередь
                            </Button>
                        )}
                    </Group>

                    <Divider size={2} my="sm" />

                    <Box style={{ position: 'relative' }}>
                        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
                            {queues.map((queue) => (
                                <Card key={queue.id} shadow="sm" padding="lg" radius="md" withBorder>
                                    <Title order={4} mb="md">{queue.title}</Title>
                                    <Text size="sm" mb={4}>Владелец: {queue.owner}</Text>
                                    <Text size="sm" mb={4}>Ближайшее окно: {queue.closestWindow}</Text>
                                    <Text size="sm" mb="lg">Длительность: {queue.duration}</Text>
                                    <Group justify="space-between" align="center">
                                        <Badge color={queue.status === 'active' ? '#5FBF24' : '#FA5252'} variant="dot">
                                            {queue.status === 'active' ? 'Активна' : 'Неактивна'}
                                        </Badge>
                                        <Button size="sm" onClick={() => handleOpenQueue(queue)}>
                                            Открыть
                                        </Button>
                                    </Group>
                                </Card>
                            ))}
                        </SimpleGrid>

                        {/* Панель просмотра очереди */}
                        {selectedQueue && (
                            <Box
                                onClick={handleClosePanel}
                                style={{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    right: 0,
                                    bottom: 0,
                                    backgroundColor: 'rgba(255, 255, 255, 0.6)',
                                    zIndex: 999,
                                    borderRadius: '8px',
                                }}
                            />
                        )}

                        {selectedQueue && (
                            <Box
                                style={{
                                    position: 'absolute',
                                    right: 0,
                                    top: 0,
                                    width: `33%`,
                                    height: `730px`,
                                    backgroundColor: 'white',
                                    boxShadow: '-2px 0 8px rgba(0, 0, 0, 0.15)',
                                    zIndex: 1000,
                                    borderRadius: '8px',
                                    overflow: 'hidden',
                                }}
                            >
                                <ScrollArea style={{ height: '100%' }}>
                                    <Paper p="lg">
                                        <Group justify="space-between" mb="md">
                                            <Title order={3}>Об очереди</Title>
                                            <ActionIcon variant="transparent" onClick={handleClosePanel} size="lg">✕</ActionIcon>
                                        </Group>
                                        <Stack gap="md">
                                            <div>
                                                <Title order={4}>{selectedQueue.title}</Title>
                                                <Text c="gray.6" fw={600} mt={4}>{selectedQueue.owner}</Text>
                                            </div>
                                            <Stack gap="xs">
                                                <div><Text size="sm" c="gray.7"><strong>Описание:</strong></Text><Text size="sm">{selectedQueue.description}</Text></div>
                                                <div><Text size="sm" c="gray.7"><strong>Длительность:</strong></Text><Text size="sm">{selectedQueue.duration}</Text></div>
                                                <div><Text size="sm" c="gray.7"><strong>Ближайшее окно:</strong></Text><Text size="sm">{selectedQueue.closestWindow}</Text></div>
                                            </Stack>
                                            <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '16px' }}>
                                                <Title order={5} mb="md">Заполните данные</Title>
                                                <Stack gap="sm">
                                                    <Text size="sm" fw={600} mb={4} c="gray.7">Дата и время начала посещения <span style={{ color: '#FA5252' }}>*</span></Text>
                                                    <TextInput placeholder="Укажите время" value={appointmentDate} onChange={(e) => setAppointmentDate(e.currentTarget.value)} />
                                                    <Text size="sm" fw={600} mb={4} c="gray.7">Время окончания посещения <span style={{ color: '#FA5252' }}>*</span></Text>
                                                    <TextInput placeholder="Укажите время" value={appointmentTime} onChange={(e) => setAppointmentTime(e.currentTarget.value)} />
                                                    <Text size="sm" fw={600} mb={4} c="gray.7">Цель <span style={{ color: '#FA5252' }}>*</span></Text>
                                                    <Textarea placeholder="Цель визита" value={visitPurpose} onChange={(e) => setVisitPurpose(e.currentTarget.value)} minRows={3} />
                                                    <div>
                                                        <Text size="sm" fw={600} mb={8}>Приложить файл</Text>
                                                        <Button variant="filled" leftSection={<IconPlus size={16} />}>Файл</Button>
                                                    </div>
                                                    <Group justify="end" mb="md">
                                                        <Button onClick={handleClosePanel}>Записаться</Button>
                                                    </Group>
                                                </Stack>
                                            </div>
                                        </Stack>
                                    </Paper>
                                </ScrollArea>
                            </Box>
                        )}

                        {/* Панель создания очереди */}
                        {showCreateQueue && (
                            <Box
                                onClick={handleCloseCreatePanel}
                                style={{
                                    position: 'absolute',
                                    top: 0,
                                    left: 0,
                                    right: 0,
                                    bottom: 0,
                                    backgroundColor: 'rgba(255, 255, 255, 0.6)',
                                    zIndex: 999,
                                    borderRadius: '8px',
                                }}
                            />
                        )}

                        {showCreateQueue && (
                            <Box
                                style={{
                                    position: 'absolute',
                                    right: 0,
                                    top: 0,
                                    width: `33%`,
                                    height: `730px`,
                                    backgroundColor: 'white',
                                    boxShadow: '-2px 0 8px rgba(0, 0, 0, 0.15)',
                                    zIndex: 1000,
                                    borderRadius: '8px',
                                    overflow: 'hidden',
                                }}
                            >
                                <ScrollArea style={{ height: '100%' }}>
                                    <Paper p="lg">
                                        <Group justify="space-between" mb="lg">
                                            <Title order={3}>Создать очередь</Title>
                                            <ActionIcon variant="transparent" onClick={handleCloseCreatePanel} size="lg">✕</ActionIcon>
                                        </Group>
                                        <Stack gap="md">
                                            <div>
                                                <Title order={5} mb="md">Основное</Title>
                                                <Stack gap="sm">
                                                    <div>
                                                        <Text size="sm" fw={600} mb={4} c="gray.7">Название <span style={{ color: '#FA5252' }}>*</span></Text>
                                                        <TextInput placeholder="Название" value={queueName} onChange={(e) => setQueueName(e.currentTarget.value)} />
                                                    </div>
                                                    <div>
                                                        <Text size="sm" fw={600} mb={4} c="gray.7">Описание <span style={{ color: '#FA5252' }}>*</span></Text>
                                                        <Textarea placeholder="Описание" value={queueDescription} onChange={(e) => setQueueDescription(e.currentTarget.value)} minRows={3} />
                                                    </div>
                                                    <div>
                                                        <Text size="sm" fw={600} mb={4} c="gray.7">Период автоочистки <span style={{ color: '#FA5252' }}>*</span></Text>
                                                        <NumberInput value={parseInt(queueAutocloseDays)} onChange={(val) => setQueueAutocloseDays(val?.toString() || '7')} min={1} />
                                                    </div>
                                                </Stack>
                                            </div>
                                            <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '16px' }}>
                                                <Title order={5} mb="md">Расписание</Title>
                                                <Stack gap="sm">
                                                    <div>
                                                        <Text size="sm" fw={600} mb={4} c="gray.7">Время начала приёма <span style={{ color: '#FA5252' }}>*</span></Text>
                                                        <TextInput placeholder="12:00" value={queueStartTime} onChange={(e) => setQueueStartTime(e.currentTarget.value)} />
                                                    </div>
                                                    <div>
                                                        <Text size="sm" fw={600} mb={4} c="gray.7">Время окончания приёма <span style={{ color: '#FA5252' }}>*</span></Text>
                                                        <TextInput placeholder="15:00" value={queueEndTime} onChange={(e) => setQueueEndTime(e.currentTarget.value)} />
                                                    </div>
                                                </Stack>
                                            </div>
                                            <Group justify="end" mb="md">
                                                <Button onClick={handleCreateQueue}>Создать</Button>
                                            </Group>
                                        </Stack>
                                    </Paper>
                                </ScrollArea>
                            </Box>
                        )}
                    </Box>
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}

export default HomePage;
