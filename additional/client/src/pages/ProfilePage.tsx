import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container, Title, Paper, TextInput, PasswordInput, Button, Stack, Group, Text, Divider, Alert, Loader, Box, SimpleGrid,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { IconBrandTelegram, IconCheck, IconLogout } from '@tabler/icons-react';
import { AppShell } from '@mantine/core';
import { Header } from '../components/Header';
import { api } from '../api/ApiClient';
import { useAuth } from '../context/AuthContext';

export default function ProfilePage() {
    const navigate = useNavigate();
    const { user, isLoading, setUser, refreshUser, logout: contextLogout } = useAuth();

    const [isProfileUpdating, setIsProfileUpdating] = useState(false);
    const [isEmailUpdating, setIsEmailUpdating] = useState(false);
    const [isPasswordUpdating, setIsPasswordUpdating] = useState(false);
    
    const [tgLink, setTgLink] = useState<string | null>(null);
    const [isTgLoading, setIsTgLoading] = useState(false);

    const profileForm = useForm({
        initialValues: { first_name: '', last_name: '', patronymic: '' },
    });

    const emailForm = useForm({
        initialValues: { new_email: '', current_password: '' },
        validate: {
            new_email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Некорректный email'),
            current_password: (value) => (value.length < 1 ? 'Введите текущий пароль' : null),
        },
        validateInputOnChange: true, 
    });

    const passwordForm = useForm({
        initialValues: { current_password: '', new_password: '', confirm_new_password: '' },
        validate: {
            current_password: (val) => (val.length < 1 ? 'Введите текущий пароль' : null),
            new_password: (val) => (val.length < 6 ? 'Пароль должен быть длиннее 6 символов' : null),
            confirm_new_password: (val, values) => (val !== values.new_password ? 'Пароли не совпадают' : null),
        },
        validateInputOnChange: true,
    });

    useEffect(() => {
        if (user) {
            if (!profileForm.isDirty()) {
                profileForm.setValues({
                    first_name: user.first_name,
                    last_name: user.last_name,
                    patronymic: user.patronymic || '',
                });
            }
        }
    }, [user]);


    const handleUpdateProfile = async (values: typeof profileForm.values) => {
        setIsProfileUpdating(true);
        try {
            await api.request('/api/v1/users/name', 'PATCH', {
                first_name: values.first_name,
                last_name: values.last_name,
                patronymic: values.patronymic.trim() === '' ? null : values.patronymic,
            });
            notifications.show({ title: 'Успех', message: 'Данные обновлены', color: 'green', icon: <IconCheck size={18} /> });
            
            if (user) {
                setUser({
                    ...user,
                    first_name: values.first_name,
                    last_name: values.last_name,
                    patronymic: values.patronymic.trim() === '' ? null : values.patronymic
                });
            }
            profileForm.resetDirty(values);
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось обновить данные', color: 'red' });
        } finally {
            setIsProfileUpdating(false);
        }
    };

    const handleUpdateEmail = async (values: typeof emailForm.values) => {
        setIsEmailUpdating(true);
        try {
            await api.request('/api/v1/users/email', 'PATCH', {
                new_email: values.new_email,
                current_password: values.current_password,
            });
            notifications.show({ title: 'Успех', message: 'Email обновлен', color: 'green', icon: <IconCheck size={18} /> });

            if (user) {
                setUser({ ...user, email: values.new_email });
            }
            emailForm.reset();
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: e.message || 'Неверный пароль или email занят', color: 'red' });
        } finally {
            setIsEmailUpdating(false);
        }
    };

    const handleUpdatePassword = async (values: typeof passwordForm.values) => {
        setIsPasswordUpdating(true);
        try {
            await api.request('/api/v1/users/password', 'PATCH', {
                old_password: values.current_password,
                new_password: values.new_password,
            });
            notifications.show({ title: 'Успех', message: 'Пароль успешно изменен', color: 'green', icon: <IconCheck size={18} /> });
            passwordForm.reset();
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: e.message || 'Не удалось изменить пароль', color: 'red' });
        } finally {
            setIsPasswordUpdating(false);
        }
    };

    const handleConnectTelegram = async () => {
        setIsTgLoading(true);
        try {
            const res = await api.request<{ link: string }>('/api/v1/users/telegram', 'GET');
            setTgLink(res.link);
            window.open(res.link, '_blank');
        } catch (e: any) {
            notifications.show({ title: 'Ошибка', message: 'Не удалось получить ссылку Telegram', color: 'red' });
        } finally {
            setIsTgLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            await api.request('/api/v1/auth/logout', 'POST');
        } catch (error) {
            console.error("Logout error", error);
        } finally {
            contextLogout();
            navigate('/');
        }
    };

    const isEmailButtonDisabled = 
        !emailForm.values.new_email || 
        !emailForm.values.current_password || 
        !emailForm.isValid();

    const isPasswordButtonDisabled = 
        !passwordForm.values.current_password || 
        !passwordForm.values.new_password || 
        !passwordForm.values.confirm_new_password || 
        !passwordForm.isValid();


    if (isLoading) {
        return (
            <AppShell header={{ height: 70 }} padding="md">
                <Header />
                <AppShell.Main>
                    <Container size="sm" py="xl">
                        <Box style={{ display: 'flex', justifyContent: 'center' }}><Loader /></Box>
                    </Container>
                </AppShell.Main>
            </AppShell>
        );
    }

    return (
        <AppShell header={{ height: 70 }} padding="md">
            <Header />
            <AppShell.Main>
                <Container size="80%" py="md">
                    <Title order={1} mb="lg">Настройки профиля</Title>
                    <Divider size={2} my="sm" />

                    <SimpleGrid cols={{ base: 1, md: 2 }} spacing="lg" verticalSpacing="lg">

                        {/* 1. Личные данные */}
                        <Paper withBorder p="md" radius="md" h="100%">
                            <Title order={4} mb="md">Личные данные</Title>
                            <form onSubmit={profileForm.onSubmit(handleUpdateProfile)}>
                                <Stack gap="md">
                                    <TextInput label="Имя" {...profileForm.getInputProps('first_name')} />
                                    <TextInput label="Фамилия" {...profileForm.getInputProps('last_name')} />
                                    <TextInput label="Отчество" {...profileForm.getInputProps('patronymic')} />
                                    <Group justify="flex-end" mt="auto">
                                        <Button 
                                            type="submit" 
                                            loading={isProfileUpdating}
                                        >
                                            Сохранить
                                        </Button>
                                    </Group>
                                </Stack>
                            </form>
                        </Paper>

                        {/* 2. Смена Email */}
                        <Paper withBorder p="md" radius="md" h="100%">
                            <Title order={4} mb="md">Смена Email</Title>
                            <Text size="sm" c="dimmed" mb="md">Текущий email: <b>{user?.email}</b></Text>
                            
                            <form onSubmit={emailForm.onSubmit(handleUpdateEmail)} style={{ height: 'calc(100% - 80px)' }}>
                                <Stack justify="space-between" h="100%">
                                    <Box>
                                        <TextInput
                                            label="Новый Email"
                                            placeholder="Введите новую электронную почту"
                                            required
                                            mb="md"
                                            {...emailForm.getInputProps('new_email')}
                                        />
                                        <PasswordInput
                                            label="Текущий пароль"
                                            placeholder="Подтвердите действие паролем"
                                            required
                                            {...emailForm.getInputProps('current_password')}
                                        />
                                    </Box>
                                    <Group justify="flex-end" mt="md">
                                        <Button 
                                            type="submit" 
                                            disabled={isEmailButtonDisabled}
                                            loading={isEmailUpdating}
                                        >
                                            Изменить Email
                                        </Button>
                                    </Group>
                                </Stack>
                            </form>
                        </Paper>

                        {/* 3. Смена Пароля */}
                        <Paper withBorder p="md" radius="md" h="100%">
                            <Title order={4} mb="md">Безопасность</Title>
                            <form onSubmit={passwordForm.onSubmit(handleUpdatePassword)}>
                                <Stack gap="md">
                                    <PasswordInput label="Текущий пароль" required placeholder="Подтвердите действие паролем" {...passwordForm.getInputProps('current_password')} />
                                    <PasswordInput label="Новый пароль" required placeholder="Введите новый пароль" {...passwordForm.getInputProps('new_password')} />
                                    <PasswordInput label="Повторите новый пароль" required placeholder="Введите новый пароль повторно" {...passwordForm.getInputProps('confirm_new_password')} />
                                    <Group justify="flex-end" mt="auto">
                                        <Button 
                                            type="submit"
                                            disabled={isPasswordButtonDisabled}
                                            loading={isPasswordUpdating}
                                        >
                                            Обновить пароль
                                        </Button>
                                    </Group>
                                </Stack>
                            </form>
                        </Paper>

                        {/* 4. Telegram + Выход */}
                        <Stack gap="lg">
                            <Paper withBorder p="md" radius="md" style={{ flex: 1 }}>
                                <Stack h="100%" justify="space-between">
                                    <div>
                                        <Group justify="space-between" mb="xs">
                                            <Title order={4}>Telegram</Title>
                                            <IconBrandTelegram size={32} color="#229ED9" />
                                        </Group>
                                        <Text size="sm" c="dimmed">Подключите Telegram для уведомлений.</Text>
                                        <Divider my="md" />
                                        {tgLink && (
                                            <Alert icon={<IconCheck size={16} />} title="Ссылка сгенерирована" color="blue" mb="md">
                                                Если переход не произошел: <a href={tgLink} target="_blank" rel="noreferrer">нажмите здесь</a>
                                            </Alert>
                                        )}
                                    </div>
                                    <Button
                                        leftSection={<IconBrandTelegram size={18} />}
                                        onClick={handleConnectTelegram}
                                        loading={isTgLoading}
                                        variant="outline"
                                        fullWidth
                                    >
                                        Подключить
                                    </Button>
                                </Stack>
                            </Paper>

                            <Paper withBorder p="md" radius="md">
                                <Group justify="space-between" mb="md">
                                    <Title order={4} c="red">Зона риска</Title>
                                    <IconLogout size={24} color="var(--mantine-color-red-6)" />
                                </Group>
                                <Text size="sm" c="dimmed" mb="md">
                                    Выход из учетной записи завершит текущую сессию.
                                </Text>
                                <Button color="red" variant="light" onClick={handleLogout} fullWidth>
                                    Выйти из аккаунта
                                </Button>
                            </Paper>
                        </Stack>
                    </SimpleGrid>
                </Container>
            </AppShell.Main>
        </AppShell>
    );
}
