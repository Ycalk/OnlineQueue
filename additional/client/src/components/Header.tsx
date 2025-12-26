import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
    Container,
    Button,
    Group,
    Title,
    Menu,
    ActionIcon,
    Text,
    AppShell
} from '@mantine/core';

import {
    IconClipboardText,
    IconFriends,
    IconChecklist,
    IconBellRinging,
    IconTransitionLeft,
    IconMenu2,
} from '@tabler/icons-react';
import { api, UserProfile } from '../api/ApiClient';

export function Header() {
    const navigate = useNavigate();
    const [user, setUser] = useState<UserProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const initUser = async () => {
            const userData = await api.getUser();
            setUser(userData);
            setIsLoading(false);
        };

        initUser();
    }, []);

    const handleLogout = async () => {
        try {
            await api.request('/api/v1/auth/logout', 'POST');
        } catch (error) {
            console.error("Logout error", error);
        } finally {
            api.clearToken();
            setUser(null);
            navigate('/authorization');
        }
    };

    return (
        <AppShell.Header>
            <Container size="100%" h="100%">
                <Group h="100%" px="md" justify="space-between">
                    <Title order={2} c="#e91e63">К Телеком</Title>

                    <Group>
                        {isLoading ? (
                            <div></div>
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
    );
}
