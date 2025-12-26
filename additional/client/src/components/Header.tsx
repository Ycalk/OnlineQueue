import { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import {
    Container,
    Button,
    Group,
    Menu,
    Text,
    AppShell,
    Image,
    ActionIcon,
    Avatar,
    rem
} from '@mantine/core';
import {
    IconClipboardText,
    IconFriends,
    IconChecklist,
    IconAdjustmentsAlt,
    IconMenu2,
} from '@tabler/icons-react';
import { useAuth } from '../context/AuthContext';

import { LoginModal } from './LoginModal';
import { RegisterModal } from './RegisterModal';

export function Header() {
    const [searchParams, setSearchParams] = useSearchParams();
    
    const { user, isLoading, refreshUser, logout: contextLogout } = useAuth(); 

    const [loginOpen, setLoginOpen] = useState(false);
    const [registerOpen, setRegisterOpen] = useState(false);

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

    const openLogin = () => setSearchParams({ action: 'login' });
    const openRegister = () => setSearchParams({ action: 'registration' });
    const closeModals = () => {
        const newParams = new URLSearchParams(searchParams);
        newParams.delete('action');
        setSearchParams(newParams);
    };
    const switchToRegister = () => setSearchParams({ action: 'registration' });


    const getUserDisplayName = () => {
        if (!user) return '';
        const fullName = `${user.last_name} ${user.first_name}`.trim();
        return fullName || user.email;
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
                                <Menu shadow="md" width={260} position="bottom-end">
                                    <Menu.Target>
                                        <ActionIcon variant="transparent" size="lg" color="gray">
                                            <IconMenu2 style={{ width: rem(28), height: rem(28) }} />
                                        </ActionIcon>
                                    </Menu.Target>

                                    <Menu.Dropdown style={{ zIndex: 1001 }}>
                                        <Menu.Item
                                            component={Link}
                                            to="/profile"
                                            style={{ textDecoration: 'none' }}
                                        >
                                            <Group gap="xs">
                                                <Avatar radius="xl" size="md">
                                                    {user.first_name?.[0]?.toUpperCase()}
                                                </Avatar>
                                                <div style={{ flex: 1, overflow: 'hidden' }}>
                                                    <Text size="sm" fw={500} truncate>
                                                        {getUserDisplayName()}
                                                    </Text>
                                                    <Text size="xs" c="dimmed" truncate>
                                                        {user.email}
                                                    </Text>
                                                </div>
                                            </Group>
                                        </Menu.Item>

                                        <Menu.Divider />

                                        <Menu.Label>Очередь</Menu.Label>
                                        <Menu.Item component={Link} to="/" leftSection={<IconClipboardText size={16} />}>
                                            Доступные очереди
                                        </Menu.Item>
                                        <Menu.Item component={Link} to="/queue/my" leftSection={<IconFriends size={16} />}>
                                            Мои очереди
                                        </Menu.Item>
                                        <Menu.Item component={Link} to="/queue/my/settings" leftSection={<IconAdjustmentsAlt size={16} />}>
                                            Управление очередями
                                        </Menu.Item>
                                        <Menu.Item component={Link} to="/application/my" leftSection={<IconChecklist size={16} />}>
                                            Мои заявки
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
                onLoginSuccess={() => { refreshUser(); closeModals(); }}
            />
            
            <RegisterModal 
                opened={registerOpen} 
                onClose={closeModals}
                onRegisterSuccess={() => { refreshUser(); closeModals(); }}
            />
        </>
    );
}
