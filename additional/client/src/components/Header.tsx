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
    Loader,
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
import { api } from '../api/ApiClient';


export interface UserProfile {
    email: string;
    first_name: string;
    last_name: string;
    patronymic: string;
}

export function Header() {
    const navigate = useNavigate();
    const [user, setUser] = useState<UserProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchUser = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setUser(null);
            setIsLoading(false);
            return;
        }

        try {
            const userData = await api.request<UserProfile>('/api/v1/users/me');
            setUser(userData);
        } catch (error) {
            console.error("Failed to fetch user profile", error);
            api.clearToken();
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();

        const unsubscribe = api.onAuthChange(() => {
            fetchUser();
        });

        return () => unsubscribe();
    }, []);

    const handleLogout = async () => {
        try {
            await api.request('/api/v1/auth/logout', 'POST');
        } catch (error) {
            console.error("Logout error", error);
        } finally {
            api.clearToken();
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
