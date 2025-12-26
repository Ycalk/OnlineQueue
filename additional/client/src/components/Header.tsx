import { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import {
    Container,
    Button,
    Group,
    Menu,
    Text,
    AppShell,
    Image,
    UnstyledButton,
} from '@mantine/core';
import {
    IconClipboardText,
    IconFriends,
    IconChecklist,
    IconBellRinging,
    IconTransitionLeft,
    IconUserCircle,
    IconChevronDown,
    IconSettings,
} from '@tabler/icons-react';
import { api, UserProfile } from '../api/ApiClient';

import { LoginModal } from './LoginModal';
import { RegisterModal } from './RegisterModal';

export function Header() {
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();

    const [user, setUser] = useState<UserProfile | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Состояния для модалок
    const [loginOpen, setLoginOpen] = useState(false);
    const [registerOpen, setRegisterOpen] = useState(false);

    // --- ЛОГИКА URL PARAMETER (action) -> MODAL ---
    useEffect(() => {
        const action = searchParams.get('action');

        if (action === 'login') {
            setLoginOpen(true);
            setRegisterOpen(false);
        } else if (action === 'registration') {
            setRegisterOpen(true);
            setLoginOpen(false);
        } else {
            setLoginOpen(false);
            setRegisterOpen(false);
        }
    }, [searchParams]);

    // --- УПРАВЛЕНИЕ URL ---

    const openLogin = () => {
        setSearchParams({ action: 'login' });
    };

    const openRegister = () => {
        setSearchParams({ action: 'registration' });
    };

    const closeModals = () => {
        // Удаляем параметр action, оставляя остальные параметры (если были)
        const newParams = new URLSearchParams(searchParams);
        newParams.delete('action');
        setSearchParams(newParams);
    };

    const switchToRegister = () => {
        setSearchParams({ action: 'registration' });
    };

    // --- ЗАГРУЗКА ДАННЫХ ---

    const loadUser = async () => {
        try {
            if (!localStorage.getItem('access_token')) {
                setUser(null);
                return;
            }
            const userData = await api.getUser();
            setUser(userData);
        } catch (e) {
            console.error(e);
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadUser();
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

    const getUserDisplayName = () => {
        if (!user) return '';
        const fullName = `${user.last_name} ${user.first_name}`.trim();
        if (fullName) {
            return (
                <>
                    <Text span fw={500}>{fullName}</Text>
                    <Text span size="xs" c="dimmed" ml={4}>({user.email})</Text>
                </>
            );
        }
        return <Text span fw={500}>{user.email}</Text>;
    };

    return (
        <>
            <AppShell.Header>
                <Container size="100%" h="100%">
                    <Group h="100%" px="md" justify="space-between">
                        <Link to="/" style={{ display: 'flex', alignItems: 'center' }}>
                            <Image
                                src="/logo.png"
                                alt="К Телеком"
                                h={30}
                                w="auto"
                                fit="contain"
                            />
                        </Link>

                        <Group>
                            {isLoading ? (
                                <div style={{ width: 100 }} />
                            ) : !user ? (
                                <>
                                    <Button onClick={openLogin} variant="outline" color='#b9bbb5ff'>
                                        Вход
                                    </Button>
                                    <Button onClick={openRegister}>
                                        Регистрация
                                    </Button>
                                </>
                            ) : (
                                <Menu shadow="md" width={260} position="bottom-end" trigger="click-hover" openDelay={100} closeDelay={200}>
                                    <Menu.Target>
                                        <UnstyledButton
                                            style={{
                                                padding: '8px 12px',
                                                borderRadius: '8px',
                                                transition: 'background-color 0.2s ease',
                                            }}
                                            onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--mantine-color-gray-1)'}
                                            onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                                        >
                                            <Group gap="xs">
                                                <div style={{ lineHeight: 1, textAlign: 'right' }}>
                                                    {getUserDisplayName()}
                                                </div>
                                                <IconChevronDown size={16} color="gray" />
                                            </Group>
                                        </UnstyledButton>
                                    </Menu.Target>

                                    <Menu.Dropdown style={{ zIndex: 1001 }}>
                                        <Menu.Label>Очередь</Menu.Label>
                                        <Menu.Item component={Link} to="/" leftSection={<IconClipboardText size={16} />}>
                                            Доступные очереди
                                        </Menu.Item>
                                        <Menu.Item component={Link} to="/queue/my" leftSection={<IconFriends size={16} />}>
                                            Мои очереди
                                        </Menu.Item>
                                        <Menu.Item component={Link} to="/queue/my/settings" leftSection={<IconSettings size={16} />}>
                                            Настройка очередей
                                        </Menu.Item>
                                        <Menu.Item component={Link} to="/application/my" leftSection={<IconChecklist size={16} />}>
                                            Мои заявки
                                        </Menu.Item>

                                        <Menu.Divider />
                                        <Menu.Label>Аккаунт</Menu.Label>

                                        <Menu.Item component={Link} to="/profile" leftSection={<IconUserCircle size={16} />}>
                                            Мой профиль
                                        </Menu.Item>

                                        <Menu.Item
                                            color="red"
                                            leftSection={<IconTransitionLeft size={16} />}
                                            onClick={handleLogout}
                                        >
                                            Выход
                                        </Menu.Item>
                                    </Menu.Dropdown>
                                </Menu>
                            )}
                        </Group>
                    </Group>
                </Container>
            </AppShell.Header>

            <LoginModal
                opened={loginOpen}
                onClose={closeModals}
                onSwitchToRegister={switchToRegister}
                onLoginSuccess={() => {
                    loadUser();
                    closeModals();
                }}
            />

            <RegisterModal
                opened={registerOpen}
                onClose={closeModals}
                onRegisterSuccess={() => {
                    loadUser();
                    closeModals();
                }}
            />
        </>
    );
}
