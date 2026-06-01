/* Corrected Code */
list_t *add_node_end(list_t *head, const int n) {
    list_t *new_node = malloc(sizeof(list_t));
    list_t *current = head;

    if (!new_node)
        return (NULL);

    new_node->n = n;
    new_node->next = NULL;

    if (!head)
        return (new_node);

    while (current->next)
        current = current->next;

    current->next = new_node;
    return (head);
}
